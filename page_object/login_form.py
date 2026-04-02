from selenium.webdriver.common.by import By
from page_object.elements.base_element import BaseElement
import allure
from page_object.base_page import BasePage


class LoginForm(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "passwd")
    SUBMIT = (By.ID, "submit_login")
    HEADER_LOGOUT = (By.CSS_SELECTOR, "#header_logout")
    EMPLOYEE_INFOS = (By.CSS_SELECTOR, "#employee_infos")

    @allure.step("Вход пользователя с username: {username}")
    def login(self, username, password):
        self.logger.info(f"Вход пользователя: {username}")
        self.send_keys_for_fields(self.EMAIL, username)
        self.send_keys_for_fields(self.PASSWORD, password)
        self.click(self.SUBMIT)

    @allure.step("Выход пользователя")
    def logout(self):
        self.logger.info("Выход пользователя")
        self.click(self.EMPLOYEE_INFOS)
        self.click(self.HEADER_LOGOUT)
