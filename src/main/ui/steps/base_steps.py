from typing import TypeVar, Iterable, Optional
import allure
from playwright.sync_api import Page
from src.main.ui.pages.base_page import BasePage

T = TypeVar("T", bound="BaseSteps")


class BaseSteps:
    def __init__(self, page: Page, page_object: Optional[BasePage] = None) -> None:
        self.page: Page = page
        self.page_object: BasePage = page_object or BasePage(page)

    @allure.step("Выход из системы")
    def logout(self: T) -> T:
        self.page_object.burger_menu.click()
        self.page_object.logout_link.wait_for()
        self.page_object.logout_link.click()
        return self

    @allure.step("Переход в корзину")
    def open_cart(self: T) -> T:
        self.page_object.cart_link.click()
        return self

    @allure.step("Проверка наличия товаров в списке")
    def check_items(self: T, expected_items: Iterable[str]) -> T:
        self.page_object.item_names.first.wait_for()
        actual_names: list[str] = [
            name.strip() for name in self.page_object.item_names.all_text_contents()
        ]
        for item in expected_items:
            with allure.step(f"Поиск товара: {item}"):
                assert item in actual_names, f"Товар '{item}' не найден в списке: {actual_names}"

        return self