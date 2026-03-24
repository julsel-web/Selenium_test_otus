from page_object.base_page import BasePage
import allure


class BaseElement(BasePage):
    @allure.step("Заполнение полей: {fields}")
    def send_keys(self, fields: dict):
        for locator, value in fields.items():
            self.logger.info(f"Ввод значения '{value}' в поле с локатором {locator}")

            element = self.wait_element_visible(locator)
            element.clear()
            element.send_keys(value)
