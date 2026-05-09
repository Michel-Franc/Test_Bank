import pytest
import random
import allure
from typing import Callable
from playwright.sync_api import Page
from src.main.ui.constants import *
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.inventory_steps import InventorySteps
from src.main.ui.steps.base_steps import BaseSteps


@pytest.fixture
def login_users(page: Page) -> Callable[[str], Page]:
    def wrapper(user_key: str) -> Page:
        LoginSteps(page).login(user_key)
        return page

    return wrapper


@pytest.fixture
def login_standard_user(login_users: Callable[[str], Page]) -> Page:
    return login_users("standard")


@pytest.fixture
def login_locked_user(page: Page) -> Page:
    login_steps = LoginSteps(page)
    login_steps.login_page.open()
    login_steps.login_page.username_input.fill(LOCKED_USER)
    login_steps.login_page.password_input.fill(PASSWORD)
    login_steps.login_page.login_button.click()
    return page


@pytest.fixture
def setup_basket(login_users: Callable[[str], Page], request: pytest.FixtureRequest) -> tuple[Page, list[str], float]:
    user_type, selection = request.param
    page = login_users(user_type)
    inventory_steps = InventorySteps(page)

    with allure.step(f"Предусловие: Подготовка корзины (Выбор: {selection})"):
        total_price: float = 0.0

        if selection == "random":
            items_to_add = random.sample(ITEMS, k=random.randint(1, len(ITEMS)))
        elif isinstance(selection, int):
            items_to_add = random.sample(ITEMS, k=selection)
        else:
            items_to_add = selection

        for item_name in items_to_add:
            data = inventory_steps.get_catalog_data(item_name)
            total_price = round(total_price + data["price"], 2)
            inventory_steps.add_to_cart(item_name)

    return page, items_to_add, round(total_price, 2)


@pytest.fixture
def clean_cart(page: Page) -> Callable[[], None]:
    def wrapper() -> None:
        BaseSteps(page).open_cart()
        remove_buttons = page.locator("button", has_text="Remove")

        with allure.step("Очистка корзины"):
            count = remove_buttons.count()
            for _ in range(count):
                remove_buttons.first.click()

    return wrapper