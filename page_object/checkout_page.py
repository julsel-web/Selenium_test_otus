from selenium.webdriver.common.by import By

from page_object.base_page import BasePage
from page_object.catalog_admin_page import CatalogAdminPage


class AssertionHelper(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    HEADER = (By.ID, "header")
    LOGIN_FORM = (By.ID, "login_form")
    MY_ACCOUNT = (By.CLASS_NAME, "account")

    def checkout_admin_page(self):
        dashboard_header = self.wait_element_visible(self.HEADER)
        assert dashboard_header.is_displayed()

    def checkout_login_page(self):
        login_form = self.wait_element_visible(self.LOGIN_FORM)
        assert login_form.is_displayed()

    def checkout_my_account(self):
        my_account = self.wait_element_visible(self.MY_ACCOUNT)
        assert my_account.is_displayed()
