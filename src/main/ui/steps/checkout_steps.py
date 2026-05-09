from typing import Optional
import allure
from playwright.sync_api import Page
from src.main.ui.steps.base_steps import BaseSteps
from src.main.ui.pages.checkout_page import CheckoutPage
from src.main.ui.helpers.ui_helpers import get_price_value


class CheckoutSteps(BaseSteps):
    def __init__(self, page: Page) -> None:
        checkout_page: CheckoutPage = CheckoutPage(page)
        super().__init__(page, page_object=checkout_page)
        self.checkout_page: CheckoutPage = checkout_page

    @allure.step("Заполнение формы доставки")
    def fill_shipping_form(self, first_name: str = "Ivan", last_name: str = "Ivanov", zip_code: str = "12345", exclude: Optional[str] = None) -> "CheckoutSteps":
        self.checkout_page.first_name_input.wait_for()

        if exclude != "first_name":
            self.checkout_page.first_name_input.fill(first_name)
        if exclude != "last_name":
            self.checkout_page.last_name_input.fill(last_name)
        if exclude != "zip_code":
            self.checkout_page.zip_code_input.fill(zip_code)

        self.checkout_page.continue_button.click()
        return self

    @allure.step("Проверка финансовых итогов заказа")
    def verify_total_price(self, expected_item_total: float) -> "CheckoutSteps":
        self.checkout_page.summary_label.wait_for()

        item_total: float = get_price_value(self.checkout_page.summary_label)
        tax: float = get_price_value(self.checkout_page.tax_label)
        total: float = get_price_value(self.checkout_page.total_label)

        with allure.step(f"Сверка суммы товаров"):
            assert item_total == expected_item_total, f"Ошибка: ожидалось {expected_item_total}, получено {item_total}"

        with allure.step(f"Проверка формулы: {item_total} + {tax} == {total}"):
            assert total == round(item_total + tax, 2), \
                f"Математическая ошибка: {item_total} + {tax} != {total}"

        return self

    @allure.step("Завершение заказа (Finish)")
    def confirm_order(self) -> "CheckoutSteps":
        self.checkout_page.finish_button.click()
        return self