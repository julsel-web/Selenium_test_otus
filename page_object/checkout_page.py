import allure
from selenium.webdriver.common.by import By
from page_object.catalog_admin_page import CatalogAdminPage
from page_object.elements.base_element import BaseElement


class CheckoutPage(BaseElement):
    HEADER = (By.ID, "header")
    LOGIN_FORM = (By.ID, "login_form")
    MY_ACCOUNT = (By.CLASS_NAME, "account")

    @allure.step("Проверка отображения админской страницы")
    def checkout_admin_page(self):
        self.logger.info("Проверка видимости HEADER на админской странице")
        dashboard_header = self.wait_element_visible(self.HEADER)
        assert dashboard_header.is_displayed()

    @allure.step("Проверка отображения страницы логина")
    def checkout_login_page(self):
        self.logger.info("Проверка видимости формы LOGIN_FORM")
        login_form = self.wait_element_visible(self.LOGIN_FORM)
        assert login_form.is_displayed()

    @allure.step("Проверка отображения страницы 'Мой аккаунт'")
    def checkout_my_account(self):
        self.logger.info("Проверка видимости элемента MY_ACCOUNT")
        my_account = self.wait_element_visible(self.MY_ACCOUNT)
        assert my_account.is_displayed()

    @allure.step("Проверка добавления продукта: {name}")
    def checkout_add_new_card(self, name):
        self.logger.info(f"Проверка наличия продукта: {name}")
        products = CatalogAdminPage(self.driver).find_all_products()
        assert name in products

    @allure.step("Проверка удаления продукта: {name}")
    def checkout_delete_product(self, name):
        self.logger.info(f"Проверка отсутствия продукта: {name}")
        products = CatalogAdminPage(self.driver).find_all_products()
        assert name not in products
