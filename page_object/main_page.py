import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from page_object.elements.base_element import BaseElement


class MainPage(BaseElement):
    PRODUCTS = (By.CSS_SELECTOR, "div.js-product")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "button[aria-label='Currency dropdown']")
    CURRENT_PRICE = (By.CSS_SELECTOR, "div.current-price")

    @allure.step("Поиск всех продуктов на странице")
    def find_products(self):
        self.logger.info(f"Поиск всех продуктов с локатором: {self.PRODUCTS}")
        self.wait_element_visible(self.PRODUCTS)
        products = self.driver.find_elements(*self.PRODUCTS)

        return products

    @allure.step("Выбор случайного продукта и переход по ссылке")
    def choose_random_product_and_get_href(self):
        products = self.find_products()

        random_product = random.choice(products)
        product_link = random_product.find_element(By.CSS_SELECTOR, "a")
        product_href = product_link.get_attribute("href")
        self.logger.info(f"Выбран продукт: {product_href}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", random_product)
        random_product.click()
        return product_href

    @allure.step("Смена валюты на {currency_code}")
    def switch_currency(self, currency_code):
        self.logger.info(f"Смена валюты на: {currency_code}")
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
        self.logger.info(f"Обновленные цены после смены валюты: {prices}")
        return prices
