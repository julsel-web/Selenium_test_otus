from selenium.webdriver.common.by import By

from page_object.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver
    ADD_TO_CART = (By.CSS_SELECTOR, "button.add-to-cart")
    BTN_PRIMARY = (By.CSS_SELECTOR, "a.btn.btn-primary[href*='cart?action=show']")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)

    def click_to_cart(self):
        self.click(self.BTN_PRIMARY)
