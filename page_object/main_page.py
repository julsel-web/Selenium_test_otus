import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from page_object.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    PRODUCTS = (By.CSS_SELECTOR, "div.js-product")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "button[aria-label='Currency dropdown']")
    CURRENT_PRICE = (By.CSS_SELECTOR, "div.current-price")

    def find_products(self):
        self.wait_element_visible(self.PRODUCTS)
        products = self.driver.find_elements(*self.PRODUCTS)

        return products

    def choose_random_product_and_get_href(self):
        products = self.find_products()

        random_product = random.choice(products)
        product_link = random_product.find_element(By.CSS_SELECTOR, "a")
        product_href = product_link.get_attribute("href")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", random_product)
        random_product.click()
        return product_href

    def switch_currency(self, currency_code):
        Currency_code = (
            By.XPATH,
            f"//div[contains(@class,'currency-selector')]//a[contains(text(),'{currency_code}')]",
        )
        self.click(self.CURRENCY_DROPDOWN)
        self.click(Currency_code)
        self.wait_until(
            lambda d: all(
                currency_code in el.text for el in d.find_elements(*self.CURRENT_PRICE)
            )
        )
        prices = [el.text for el in self.driver.find_elements(*self.CURRENT_PRICE)]
        return prices
