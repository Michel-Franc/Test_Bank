import pytest
import allure
from typing import List, Dict, Any, Tuple
from playwright.sync_api import expect, Page
from src.main.ui.constants import *
from src.main.ui.steps.inventory_steps import InventorySteps


@pytest.mark.ui
@allure.suite("Тесты каталога товаров")
class TestCatalog:
    @allure.title("Проверка общего количества товаров")
    def test_count_catalog(self, login_standard_user: Page) -> None:
        InventorySteps(login_standard_user).check_items(ITEMS)

    @allure.title("Сортировка товаров по названию")
    @pytest.mark.parametrize("sort_type, reverse", [("az", False), ("za", True)])
    def test_sort_by_name(self, login_standard_user: Page, sort_type: str, reverse: bool) -> None:
        inventory: InventorySteps = InventorySteps(login_standard_user)
        inventory.sort_products(sort_type)

        inventory.inventory_page.item_names.first.wait_for()
        names: List[str] = inventory.inventory_page.item_names.all_text_contents()

        actual_names: List[str] = [n.strip() for n in names]
        with allure.step(f"Проверка: {actual_names} отсортированы (reverse={reverse})"):
            assert actual_names == sorted(actual_names, reverse=reverse)

    @allure.title("Сортировка товаров по цене")
    @pytest.mark.parametrize("sort_type, reverse", [("lohi", False), ("hilo", True)])
    def test_sort_by_price(self, login_standard_user: Page, sort_type: str, reverse: bool) -> None:
        InventorySteps(login_standard_user).sort_products(sort_type).should_see_correct_prices(reverse=reverse)

    @allure.title("Соответствие данных каталога и карточки")
    def test_all_products_details(self, login_standard_user: Page) -> None:
        inventory: InventorySteps = InventorySteps(login_standard_user)

        for item_name in ITEMS[:3]:
            catalog_data: Dict[str, Any] = inventory.get_catalog_data(item_name)
            card_data: Dict[str, Any] = inventory.open_product_details(item_name).get_details_from_card()

            with allure.step(f"Сверка данных для: {item_name}"):
                assert card_data["name"] == catalog_data["name"]
                assert card_data["price"] == catalog_data["price"]

            inventory.go_back_to_catalog()

    @allure.title("Проверка работы кнопок Add/Remove в каталоге")
    @pytest.mark.parametrize("setup_basket", [("standard", "random")], indirect=True)
    def test_catalog_buttons(self, setup_basket: Tuple[Page, List[str], float]) -> None:
        page, items_list, _ = setup_basket
        inventory: InventorySteps = InventorySteps(page)

        expect(inventory.inventory_page.cart_badge).to_have_text(str(len(items_list)))

        for item_name in items_list:
            inventory.remove_from_cart(item_name)

        with allure.step("Проверка: счетчик корзины исчез"):
            expect(inventory.inventory_page.cart_badge).not_to_be_visible()





