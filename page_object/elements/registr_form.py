from selenium.webdriver.common.by import By

from page_object.elements.base_element import BaseElement


class ReristForm(BaseElement):
    Ft_name = (By.ID, "field-firstname")
    LT_name = (By.ID, "field-lastname")
    Email = (By.ID, "field-email")
    Password = (By.ID, "field-password")
    Hb = (By.ID, "field-birthday")
    Save_button = (
        By.CSS_SELECTOR,
        "footer.form-footer button.btn.btn-primary.form-control-submit",
    )
    Checkbox_psgdr = (By.XPATH, "//input[@name='psgdpr']/following-sibling::span")
    Checkbox_privacy = (By.XPATH, "//input[@name='customer_privacy']/..")

    def registr(self, Gender, Ft_name, LT_name, Email, Password, Hb):
        gender = (
            By.XPATH,
            f"//label[contains(@class, 'radio-inline') and contains(., '{Gender}')]",
        )
        self.click(gender)

        registr_items = {
            self.Ft_name: Ft_name,
            self.LT_name: LT_name,
            self.Email: Email,
            self.Password: Password,
            self.Hb: Hb,
        }
        self.send_keys(registr_items)
        for checkbox in [self.Checkbox_psgdr, self.Checkbox_privacy]:
            self.click_element_safe(checkbox)

        self.click_element_safe(self.Save_button)
