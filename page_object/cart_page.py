from selenium.webdriver.common.by import By

from page_object.elements.base_element import BaseElement


class CartPage(BaseElement):
    PRODUCT_TO_CART = (By.CSS_SELECTOR, "div.product-line-info a.label")

    def check_card_to_cart(self):
        card = self.wait_element_visible(self.PRODUCT_TO_CART)
        return card
