import allure
from playwright.sync_api import Page, Locator
from src.main.ui.constants import *


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.burger_menu: Locator = page.locator(BURGER_MENU)
        self.logout_link: Locator = page.locator(LOGOUT)
        self.cart_link: Locator = page.locator(CART_LINK)
        self.item_names: Locator = page.locator(ITEM_NAME)

    def navigate(self, url: str) -> None:
        with allure.step(f"Переход по адресу: {url}"):
            self.page.goto(url, wait_until="domcontentloaded")