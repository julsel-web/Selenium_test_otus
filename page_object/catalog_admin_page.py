
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from page_object.base_page import BasePage

class CatalogAdminPage(BasePage):
    def __init__(self, page: BasePage):
        self.page = page
        self.driver = page.driver

    CATALOG = (By.CSS_SELECTOR, "#subtab-AdminCatalog")
    PRODUCTS = (By.CSS_SELECTOR, "#subtab-AdminProducts > a")
    All_PRODUCTS = (By.CSS_SELECTOR, "a.text-primary.text-nowrap")
    BTN_NEXT = (By.CSS_SELECTOR, "#pagination_next_url")
    ADD_NEW_CARD = (By.CSS_SELECTOR, "#page-header-desc-configuration-add")
    ADD_NEW_PRODUCT = (By.CSS_SELECTOR, "#create_product_create")
    NAME_IFRAME = (By.NAME, "modal-create-product-iframe")
    NAME_CARD = (By.CSS_SELECTOR, "#product_header_name_1")
    BTN_SAVE = (By.CSS_SELECTOR, "#product_footer_save")
    GO_TO_CATALOG = (By.CSS_SELECTOR, "#product_footer_actions_catalog")
    BTN_TPGGLE = (By.CSS_SELECTOR, "#product_footer_actions_dropdown")
    DELETE_PRODUCT = (By.CSS_SELECTOR, "#product_footer_actions_delete")
    BTN_DELETE = (By.XPATH, "//button[normalize-space(text())='Delete']")

    @allure.step("Переход на страницу каталога")
    def catalog_page(self):
        self.logger.info("Переход на страницу каталога")
        self.click(self.CATALOG)

    @allure.step("Переход на страницу продуктов")
    def products_page(self):
        self.logger.info("Переход на страницу продуктов")
        self.click_element_safe(self.PRODUCTS)

    @allure.step("Поиск всех продуктов на текущей странице")
    def find_all_products(self):
        self.logger.info("Поиск всех продуктов на текущей странице")
        self.wait_element_visible(self.AllPRODUCTS)
        products = self.driver.find_elements(*self.AllPRODUCTS)
        return [el.text.strip() for el in products]

    @allure.step("Проверка наличия следующей страницы")
    def has_next_page(self):
        has_next = len(self.driver.find_elements(*self.BTNNEXT)) > 0
        self.logger.info(f"Есть следующая страница: {has_next}")
        return has_next

    @allure.step("Переход на следующую страницу")
    def go_to_next_page(self):
        self.logger.info("Переход на следующую страницу")
        next_btn = self.wait_element_visible(self.BTNNEXT)
        self.click(self.BTNNEXT)
        self.wait_until(
            EC.staleness_of(self.driver.find_elements(*self.All_PRODUCTS)[0])
        )

    @allure.step("Получение всех продуктов каталога")
    def get_all_products(self):
        self.logger.info("Получение всех продуктов каталога")
        all_products = []

        while True:
            all_products.extend(self.find_all_products())

            if self.has_next_page():
                self.go_to_next_page()
            else:
                break

        return all_products

    @allure.step("Добавление нового продукта: {name}")
    def add_new_products(self, value, name):
        self.logger.info(f"Добавление нового продукта: {name}")
        BTN_PRIMARY = (By.CSS_SELECTOR, f'button[data-value="{value}"]')
        self.click(self.ADD_NEW_CARD)
        iframe = self.driver.find_element(*self.NAME_IFRAME)
        self.driver.switch_to.frame(iframe)
        self.click_element_safe(BTN_PRIMARY)
        self.click(self.ADD_NEW_PRODUCT)
        self.driver.switch_to.default_content()
        self.send_keys_for_fields(self.NAME_CARD, name)
        self.click(self.BTN_SAVE)
        self.wait_until(
            lambda d: d.find_element(*self.GO_TO_CATALOG).is_displayed()
            and d.find_element(*self.GO_TO_CATALOG).is_enabled()
        )

        self.click(self.GOTOCATALOG)
        self.logger.info(f"Продукт {name} добавлен")
        return name

    @allure.step("Проверка добавления продукта: {name}")
    def checkout_add_new_card(self, name):
        self.logger.info(f"Проверка наличия продукта: {name}")
        products = self.find_all_products()
        assert name in products

    @allure.step("Удаление продукта: {product_name}")
    def delete_products(self, product_name):
        self.logger.info(f"Удаление продукта: {product_name}")
        row = (By.XPATH, f"//td[@class='link-type column-name text-left']/a[normalize-space(text())='{product_name}']")
        self.click_element_safe(row)
        self.click(self.BTNTPGGLE)
        self.click(self.DELETEPRODUCT)
        self.click(self.BTNDELETE)
        self.logger.info(f"Продукт {product_name} удалён")
        return product_name

    @allure.step("Проверка удаления продукта: {name}")
    def checkout_delete_product(self, name):
        self.logger.info(f"Проверка отсутствия продукта: {name}")
        self.click(self.GO_TO_CATALOG)
        assert name not in products
