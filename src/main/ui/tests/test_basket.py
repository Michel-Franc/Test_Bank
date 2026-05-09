import pytest
import allure
from typing import Callable, List, Tuple
from playwright.sync_api import expect, Page
from src.main.ui.constants import *
from src.main.ui.steps.base_steps import BaseSteps


@pytest.mark.ui
@allure.suite("Тесты корзины")
class TestBasket:
    @allure.title("Проверка добавления товаров в корзину")
    @pytest.mark.parametrize("setup_basket", [("standard", "random")], indirect=True)
    def test_add_items(self, setup_basket: Tuple[Page, List[str], float]) -> None:
        page, add_items, _ = setup_basket
        BaseSteps(page).open_cart().check_items(add_items)

    @allure.title("Удаление всех товаров из корзины")
    @pytest.mark.parametrize("setup_basket", [("standard", 3)], indirect=True)
    def test_remove_item(self, setup_basket: Tuple[Page, List[str], float], clean_cart: Callable[[], None]) -> None:
        page, add_items, _ = setup_basket
        steps: BaseSteps = BaseSteps(page)

        steps.open_cart().check_items(add_items)

        clean_cart()

        with allure.step("Проверка, что корзина пуста"):
            expect(page.locator(CART_ITEM)).to_have_count(0)
            expect(page.locator(CART_BADGE)).not_to_be_visible()

    @allure.title("Жизненный цикл корзины: добавление и полная очистка")
    @pytest.mark.parametrize("setup_basket", [("standard", "random")], indirect=True)
    def test_cart_lifecycle(self, setup_basket: Tuple[Page, List[str], float], clean_cart: Callable[[], None]) -> None:
        page, add_items, _ = setup_basket

        BaseSteps(page).open_cart().check_items(add_items)
        clean_cart()

        with allure.step("Проверка отсутствия товаров и счетчика"):
            expect(page.locator(CART_ITEM)).to_have_count(0)
            expect(page.locator(CART_BADGE)).not_to_be_visible()