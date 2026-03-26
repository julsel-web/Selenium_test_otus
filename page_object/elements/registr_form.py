from selenium.webdriver.common.by import By

from page_object.base_page import BasePage
from page_object.elements.base_element import BaseElement


class RegistrationForm(BaseElement):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    FIRST_NAME = (By.ID, "field-firstname")
    LAST_NAME = (By.ID, "field-lastname")
    EMAIL = (By.ID, "field-email")
    PASSWORD= (By.ID, "field-password")
    HAPPY_BIRTHDAY = (By.ID, "field-birthday")
    SAVE_BUTTON= (
        By.CSS_SELECTOR,
        "footer.form-footer button.btn.btn-primary.form-control-submit",
    )
    CHECKBOX_PSGDR = (By.XPATH, "//input[@name='psgdpr']/following-sibling::span")
    CHECKBOX_PRIVACY = (By.XPATH, "//input[@name='customer_privacy']/..")

    def registration(self, Gender, First_name, Last_name, Email, Password, Happy_Birthday):
        gender = (
            By.XPATH,
            f"//label[contains(@class, 'radio-inline') and contains(., '{Gender}')]",
        )
        self.click(gender)
        self.send_keys_for_fields(self.FIRST_NAME, First_name)
        self.send_keys_for_fields(self.LAST_NAME, Last_name)
        self.send_keys_for_fields(self.EMAIL, Email)
        self.send_keys_for_fields(self.PASSWORD, Password)
        self.send_keys_for_fields(self.HAPPY_BIRTHDAY, Happy_Birthday)
        for checkbox in [self.CHECKBOX_PSGDR, self.CHECKBOX_PRIVACY]:
            self.click_element_safe(checkbox)

        self.click_element_safe(self.SAVE_BUTTON)
