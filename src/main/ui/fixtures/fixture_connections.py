import pytest
import allure
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_instance():
    with allure.step("Инициализация Playwright"):
        with sync_playwright() as playwright:
            yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance):
    with allure.step("Запуск браузера Chromium"):
        browser = playwright_instance.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    with allure.step("Создание нового контекста и страницы"):
        context = browser.new_context()
        context.set_default_timeout(15000)
        context.set_default_navigation_timeout(15000)
        page = context.new_page()
        yield page
        context.close()