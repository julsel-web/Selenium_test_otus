from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logger import get_logger
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)

    @allure.step("Клик по элементу {locator} с паузой {pause}")
    def click(self, locator: tuple, pause=0.3):
        self.logger.info(f"Клик по элементу: {locator} с паузой {pause}")
        ActionChains(self.driver).move_to_element(
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            )
        ).pause(pause).click().perform()

    @allure.step("Безопасный клик по элементу {locator} с паузой {pause}")
    def click_element_safe(self, locator: tuple, pause=0.1):
        self.logger.info(f"Безопасный клик по элементу: {locator} с паузой {pause}")
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'auto', block:'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ожидание видимости элемента {locator}")
    def wait_element_visible(self, locator: tuple):
        self.logger.info(f"Ожидание видимости элемента: {locator}")
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание условия {condition}")
    def wait_until(self, condition):
        self.logger.info(f"Ожидание условия: {condition}")
        return WebDriverWait(self.driver, 5).until(condition)
