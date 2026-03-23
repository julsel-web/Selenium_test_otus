import random
from os import wait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page_object.elements.base_element import BaseElement


class CatalogAdminPage(BaseElement):
    CATALOG = (By.CSS_SELECTOR, "#subtab-AdminCatalog")
    PRODUCTS = (By.CSS_SELECTOR, "#subtab-AdminProducts > a")
    AllPRODUCTS = (By.CSS_SELECTOR, "a.text-primary.text-nowrap")
    BTNNEXT = (By.CSS_SELECTOR, "#pagination_next_url")
    ADDNEWCARD = (By.CSS_SELECTOR, "#page-header-desc-configuration-add")
    ADDNEWPRODUCT = (By.CSS_SELECTOR, "#create_product_create")
    NAMEIFRAME = (By.NAME, "modal-create-product-iframe")
    NAMECARD = (By.CSS_SELECTOR, "#product_header_name_1")
    BTNSAVE = (By.CSS_SELECTOR, "#product_footer_save")
    GOTOCATALOG = (By.CSS_SELECTOR, "#product_footer_actions_catalog")
    BTNTPGGLE = (By.CSS_SELECTOR, "#product_footer_actions_dropdown")
    DELETEPRODUCT = (By.CSS_SELECTOR, "#product_footer_actions_delete")
    BTNDELETE = (By.XPATH, "//button[normalize-space(text())='Delete']")

    def catalog_page(self):
        self.click(self.CATALOG)

    def products_page(self):
        self.click_element_safe(self.PRODUCTS)

    def find_all_products(self):
        self.wait_element_visible(self.AllPRODUCTS)
        products = self.driver.find_elements(*self.AllPRODUCTS)
        return [el.text.strip() for el in products]

    def has_next_page(self):
        return len(self.driver.find_elements(*self.BTNNEXT)) > 0

    def go_to_next_page(self):
        next_btn = self.wait_element_visible(self.BTNNEXT)
        self.click(self.BTNNEXT)
        self.wait_until(
            EC.staleness_of(self.driver.find_elements(*self.AllPRODUCTS)[0])
        )

    def get_all_products(self):
        all_products = []

        while True:
            all_products.extend(self.find_all_products())

            if self.has_next_page():
                self.go_to_next_page()
            else:
                break

        return all_products

    def add_new_products(self, value, name):
        BTN_PRIMARY = (By.CSS_SELECTOR, f'button[data-value="{value}"]')
        self.click(self.ADDNEWCARD)
        iframe = self.driver.find_element(*self.NAMEIFRAME)
        self.driver.switch_to.frame(iframe)
        self.click_element_safe(BTN_PRIMARY)
        self.click(self.ADDNEWPRODUCT)
        self.driver.switch_to.default_content()
        product_items = {self.NAMECARD: name}

        self.send_keys(product_items)
        self.click(self.BTNSAVE)
        self.wait_until(
            lambda d: d.find_element(*self.GOTOCATALOG).is_displayed()
            and d.find_element(*self.GOTOCATALOG).is_enabled()
        )
        self.click(self.GOTOCATALOG)
        return name

    def delete_products(self, product_name):
        row = (By.XPATH, f"//a[normalize-space(text())='{product_name}']/ancestor::tr")
        delete_product = self.driver.find_element(*row)
        delete_product.click()
        self.click(self.BTNTPGGLE)
        self.click(self.DELETEPRODUCT)
        self.click(self.BTNDELETE)
        return product_name
