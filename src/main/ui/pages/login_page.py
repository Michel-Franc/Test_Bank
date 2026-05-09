from playwright.sync_api import Page, Locator
from src.main.ui.pages.base_page import BasePage
from src.main.ui.constants import *


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.get_by_placeholder("Username")
        self.password_input: Locator = page.get_by_placeholder("Password")

        self.login_button: Locator = page.locator(LOGIN_BUTTON)
        self.error_message: Locator = page.locator(ERROR_MESSAGE)

    def open(self) -> None:
        self.navigate(BASE_URL)
        self.username_input.wait_for()