import allure
from selenium.webdriver.common.by import By
from page_object.base_page import BasePage

class AssertionHelper(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

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
