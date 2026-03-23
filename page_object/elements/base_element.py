from page_object.base_page import BasePage


class BaseElement(BasePage):
    def send_keys(self, fields: dict):
        for locator, value in fields.items():
            element = self.wait_element_visible(locator)
            element.clear()
            element.send_keys(value)
