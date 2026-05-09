import allure
from playwright.sync_api import Page
from src.main.ui.steps.base_steps import BaseSteps
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.constants import *


class LoginSteps(BaseSteps):
    def __init__(self, page: Page) -> None:
        login_page: LoginPage = LoginPage(page)
        super().__init__(page, page_object=login_page)
        self.login_page: LoginPage = login_page

    @allure.step("Авторизация под пользователем: {user_key}")
    def login(self, user_key: str) -> "LoginSteps":
        username: str = USERS.get(user_key, user_key)
        self.login_page.open()
        self.login_page.username_input.fill(username)
        self.login_page.password_input.fill(PASSWORD)

        with self.page.expect_navigation(url=INVENTORY_URL):
            self.login_page.login_button.click()
        return self

    @allure.step("Проверка текста ошибки")
    def check_error_text(self, expected_text: str) -> "LoginSteps":
        self.login_page.error_message.wait_for()
        actual_error: str = self.login_page.error_message.inner_text()
        assert expected_text in actual_error, f"Ожидали '{expected_text}', но получили '{actual_error}'"
        return self