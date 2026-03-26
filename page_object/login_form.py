from selenium.webdriver.common.by import By

from page_object.base_page import BasePage
from page_object.elements.base_element import BaseElement


class LoginForm(BaseElement):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "passwd")
    SUBMIT = (By.ID, "submit_login")
    HEADER_LOGOUT = (By.CSS_SELECTOR, "#header_logout")
    EMPLOYEE_INFOS = (By.CSS_SELECTOR, "#employee_infos")

    def login(self, email, password):
        self.send_keys_for_fields(self.EMAIL, email)
        self.send_keys_for_fields(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def logout(self):
        self.click(self.EMPLOYEE_INFOS)
        self.click(self.HEADER_LOGOUT)
