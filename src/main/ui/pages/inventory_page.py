from playwright.sync_api import Page, Locator
from src.main.ui.pages.base_page import BasePage
from src.main.ui.constants import *

class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sort_dropdown: Locator = page.locator(SORT_MENU)
        self.item_prices: Locator = page.locator(PRICE_LIST)
        self.cart_badge: Locator = page.locator(CART_BADGE)

    def get_card(self, item_name: str) -> Locator:
        return self.page.locator(ITEM_CONTAINER).filter(has_text=item_name).first