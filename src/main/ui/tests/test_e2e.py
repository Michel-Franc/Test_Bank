import pytest
import allure
from typing import List, Tuple
from playwright.sync_api import expect, Page
from src.main.ui.constants import *
from src.main.ui.steps.checkout_steps import CheckoutSteps


@pytest.mark.ui
@allure.suite("E2E Сценарии покупки")
class TestE2E:
    @allure.title("Положительный сценарий: Покупка товаров")
    @allure.description("Проверка состава корзины, налогов и итоговой суммы")
    @pytest.mark.parametrize("setup_basket", [("standard", "random")], indirect=True)
    def test_e2e_valid(self, setup_basket: Tuple[Page, List[str], float]) -> None:
        page, add_items, expected_total = setup_basket
        checkout_steps: CheckoutSteps = CheckoutSteps(page)

        checkout_steps.open_cart().check_items(add_items)

        with allure.step("Переход к оформлению (Checkout)"):
            page.locator(CHECKOUT).click()

        checkout_steps.fill_shipping_form().verify_total_price(expected_total)
        checkout_steps.confirm_order()

        with allure.step("Проверка успешного завершения заказа"):
            expect(page.locator(COMPLETE_HEADER)).to_have_text("Thank you for your order!")

    @allure.title("Негативный сценарий: Валидация обязательных полей")
    @pytest.mark.parametrize("setup_basket", [("standard", 1)], indirect=True)
    @pytest.mark.parametrize("empty_field, error_text", CHECKOUT_ERRORS)
    def test_checkout_negative(self, setup_basket: Tuple[Page, List[str], float], empty_field: str, error_text: str) -> None:
        page, _, _ = setup_basket
        checkout_steps: CheckoutSteps = CheckoutSteps(page)
        checkout_steps.open_cart()

        with allure.step("Переход к оформлению"):
            page.locator(CHECKOUT).click()

        checkout_steps.fill_shipping_form(exclude=empty_field)

        with allure.step(f"Проверка сообщения об ошибке для поля: {empty_field}"):
            error_message = page.locator(ERROR_MESSAGE)
            expect(error_message).to_be_visible()
            expect(error_message).to_have_text(error_text)