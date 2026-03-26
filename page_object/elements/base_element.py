from page_object.base_page import BasePage


class BaseElement(BasePage):
    def send_keys_for_fields(self, locator,value):
        element = self.wait_element_visible(locator)
        element.clear()
        element.send_keys(value)
