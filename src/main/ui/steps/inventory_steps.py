import allure
from typing import Dict, Any, List
from playwright.sync_api import Page, expect
from src.main.ui.steps.base_steps import BaseSteps
from src.main.ui.pages.inventory_page import InventoryPage
from src.main.ui.helpers.ui_helpers import get_price_value
from src.main.ui.constants import *

class InventorySteps(BaseSteps):
    def __init__(self, page: Page) -> None:
        inventory_page: InventoryPage = InventoryPage(page)
        super().__init__(page, page_object=inventory_page)
        self.inventory_page: InventoryPage = inventory_page

    @allure.step("Сортировка товаров: {sort_type}")
    def sort_products(self, sort_type: str) -> "InventorySteps":
        self.inventory_page.sort_dropdown.select_option(sort_type)
        self.inventory_page.item_names.first.wait_for()
        return self

    @allure.step("Добавление '{item_name}' в корзину")
    def add_to_cart(self, item_name: str) -> "InventorySteps":
        card = self.inventory_page.get_card(item_name)
        card.locator("button", has_text="Add to cart").click()
        return self

    @allure.step("Проверка сортировки цен")
    def should_see_correct_prices(self, reverse: bool = False) -> "InventorySteps":
        self.inventory_page.item_prices.first.wait_for()
        raw_prices: List[str] = self.inventory_page.item_prices.all_text_contents()
        prices: List[float] = get_price_value(raw_prices)
        assert prices == sorted(prices, reverse=reverse), f"Цены не отсортированы: {prices}"
        return self

    @allure.step("Сбор данных товара '{item_name}'")
    def get_catalog_data(self, item_name: str) -> Dict[str, Any]:
        card = self.inventory_page.get_card(item_name)
        card.wait_for()
        return {
            "name": card.locator(ITEM_NAME).inner_text().strip(),
            "price": get_price_value(card.locator(ITEM_PRICE))
        }

    @allure.step("Переход в карточку товара: {item_name}")
    def open_product_details(self, item_name: str) -> "InventorySteps":
        card = self.inventory_page.get_card(item_name)
        card.locator(ITEM_NAME).click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    @allure.step("Сбор данных из карточки")
    def get_details_from_card(self) -> Dict[str, Any]:
        return {
            "name": self.page.locator(ITEM_NAME).inner_text().strip(),
            "price": get_price_value(self.page.locator(ITEM_PRICE))
        }

    @allure.step("Возврат в каталог")
    def go_back_to_catalog(self) -> "InventorySteps":
        self.page.go_back()
        expect(self.page).to_have_url(INVENTORY_URL)
        return self

    @allure.step("Удаление '{item_name}' из корзины")
    def remove_from_cart(self, item_name: str) -> "InventorySteps":
        card = self.inventory_page.get_card(item_name)
        card.locator("button", has_text="Remove").click()
        return self