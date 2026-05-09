
BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL = f"{BASE_URL}inventory.html"


PASSWORD = "secret_sauce"
USERS = {
    "standard": "standard_user",
    "problem": "problem_user",
    "glitch": "performance_glitch_user",
    "error": "error_user",
    "visual": "visual_user"
}
LOCKED_USER = "locked_out_user"

ITEMS = [
    "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"
]


LOGIN_BUTTON = "#login-button"
BURGER_MENU = "#react-burger-menu-btn"
LOGOUT = "#logout_sidebar_link"
SORT_MENU = ".product_sort_container"
PRICE_LIST = ".inventory_item_price"
ITEM_CONTAINER = ".inventory_item"
CART_LINK = ".shopping_cart_link"
CART_BADGE = ".shopping_cart_badge"
CART_ITEM = ".cart_item"
ITEM_NAME = "[data-test='inventory-item-name']"
ITEM_PRICE = "[data-test='inventory-item-price']"


CHECKOUT = "#checkout"
CONTINUE = "#continue"
SUMMARY = ".summary_subtotal_label"
TAX = ".summary_tax_label"
TOTAL = ".summary_total_label"
FINISH = "#finish"
FIRST_NAME_INPUT = "#first-name"
LAST_NAME_INPUT = "#last-name"
POSTAL_CODE_INPUT = "#postal-code"
COMPLETE_HEADER = ".complete-header"

ERROR_MESSAGE = "[data-test='error']"
CHECKOUT_ERRORS = [
    ("first_name", "Error: First Name is required"),
    ("last_name", "Error: Last Name is required"),
    ("zip_code", "Error: Postal Code is required")
]