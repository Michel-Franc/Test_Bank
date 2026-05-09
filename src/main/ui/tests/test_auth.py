import pytest
import allure
from typing import Callable
from playwright.sync_api import expect, Page
from src.main.ui.constants import *
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.base_steps import BaseSteps


@pytest.mark.ui
@allure.suite("Тесты авторизации")
class TestLoginUsers:
    @allure.title("Успешный вход под разными ролями")
    @pytest.mark.parametrize("user_key", USERS.keys())
    def test_login_success(self, login_users: Callable[[str], Page], user_key: str) -> None:
        page: Page = login_users(user_key)

        with allure.step(f"Финальная проверка URL: {INVENTORY_URL}"):
            expect(page).to_have_url(INVENTORY_URL)

    @allure.title("Ошибка при входе заблокированным пользователем")
    def test_login_locked_user(self, login_locked_user: Page) -> None:
        LoginSteps(login_locked_user).check_error_text("Sorry, this user has been locked out")


@pytest.mark.ui
@allure.suite("Тесты выхода из системы")
class TestLogoutUsers:
    @allure.title("Успешный Logout из системы")
    @pytest.mark.parametrize("user_key", ["standard"])
    def test_logout_users(self, login_users: Callable[[str], Page], user_key: str) -> None:
        page: Page = login_users(user_key)

        BaseSteps(page).logout()

        with allure.step("Проверка возврата на страницу логина"):
            expect(page).to_have_url(BASE_URL)