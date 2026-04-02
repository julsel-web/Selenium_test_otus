from selenium.webdriver.common.by import By
import allure
from page_object.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    PRODUCT_TO_CART = (By.CSS_SELECTOR, "div.product-line-info a.label")

    @allure.step("Проверка товара в корзине")
    def check_card_to_cart(self):
        self.logger.info(f"Проверка наличия товара с локатором: {self.PRODUCT_TO_CART}")
        card = self.wait_element_visible(self.PRODUCT_TO_CART)
        return card
