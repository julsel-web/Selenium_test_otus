from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator: tuple, pause=0.3):
        ActionChains(self.driver).move_to_element(
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            )
        ).pause(pause).click().perform()

    def click_element_safe(self, locator: tuple, pause=0.1):
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'auto', block:'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

    def wait_element_visible(self, locator: tuple):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until(self, condition):
        return WebDriverWait(self.driver, 5).until(condition)
