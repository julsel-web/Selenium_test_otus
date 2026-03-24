from selenium.webdriver.common.by import By
import allure
from page_object.elements.base_element import BaseElement


class ProductPage(BaseElement):
    ADD_TO_CART = (By.CSS_SELECTOR, "button.add-to-cart")
    BTN_PRIMARY = (By.CSS_SELECTOR, "a.btn.btn-primary[href*='cart?action=show']")

    @allure.step("Добавление товара в корзину")
    def add_to_cart(self):
        self.logger.info(f"Клик по кнопке добавления в корзину: {self.ADD_TO_CART}")
        self.click(self.ADD_TO_CART)

    @allure.step("Переход в корзину")
    def click_to_cart(self):
        self.logger.info(f"Переход в корзину по кнопке: {self.BTN_PRIMARY}")
        self.click(self.BTN_PRIMARY)
