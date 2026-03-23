from selenium.webdriver.common.by import By

from page_object.elements.base_element import BaseElement


class LoginForm(BaseElement):
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "passwd")
    SUBMIT = (By.ID, "submit_login")
    HEADER_LOGOUT = (By.CSS_SELECTOR, "#header_logout")
    EMPLOYEE_INFOS = (By.CSS_SELECTOR, "#employee_infos")

    def login(self, username, password):
        login_items = {
            self.EMAIL: username,
            self.PASSWORD: password,
        }

        self.send_keys(login_items)
        self.click(self.SUBMIT)

    def logout(self):
        self.click(self.EMPLOYEE_INFOS)
        self.click(self.HEADER_LOGOUT)
