from playwright.sync_api import Page, Locator
from src.main.ui.pages.base_page import BasePage
from src.main.ui.constants import *


class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.first_name_input: Locator = page.locator(FIRST_NAME_INPUT)
        self.last_name_input: Locator = page.locator(LAST_NAME_INPUT)
        self.zip_code_input: Locator = page.locator(POSTAL_CODE_INPUT)

        self.continue_button: Locator = page.locator(CONTINUE)
        self.finish_button: Locator = page.locator(FINISH)

        self.summary_label: Locator = page.locator(SUMMARY)
        self.tax_label: Locator = page.locator(TAX)
        self.total_label: Locator = page.locator(TOTAL)