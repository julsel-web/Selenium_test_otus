"""import pytest
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 5)

#Написать автотест логина-разлогина в админку с проверкой, что логин был выполнен
def test_admin_login_logout(driver, base_url, wait):
    driver.get(f"{base_url}/administration")
#Ввести почту
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.send_keys("admin@example.com")
    # Ввести пароль
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "passwd")))
    password_input.send_keys("Admin123!")

    login_button = wait.until(EC.visibility_of_element_located((By.ID, "submit_login")))

    login_button.click()
    # Залогиниться
    dashboard_header = wait.until(EC.visibility_of_element_located((By.ID, "header")))
    assert dashboard_header.is_displayed()
    # Разлогиниться
    profile = wait.until(EC.visibility_of_element_located((By.ID, "employee_infos")))
    profile.click()

    header_logout = wait.until(EC.visibility_of_element_located((By.ID, "header_logout")))
    header_logout.click()


    login_form = wait.until(EC.visibility_of_element_located((By.ID, "login_form")))
    assert login_form.is_displayed()


#Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине

def test_homepage_elements(driver, base_url, wait):
    driver.get(base_url)
    # Найти товар на главном экране
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.js-product")))

    random_product = random.choice(products)

    product_link = random_product.find_element(By.CSS_SELECTOR, "a")
    product_href = product_link.get_attribute("href")

    driver.execute_script("arguments[0].scrollIntoView(true);", random_product)
    random_product.click()
    # Добавить товар в корзину
    add_to_cart = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.add-to-cart")))
    add_to_cart.click()
    # Перейти в корзину
    proceed_to_checkout = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href*='cart?action=show']")))
    proceed_to_checkout.click()
    # ПРоверить, что в корзине лежит тот же товар
    product_cat = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-line-info a.label")))
    cart_href = product_cat.get_attribute("href")


    assert cart_href  == product_href



#Проверить, что при переключении валют цены на товары меняются на главной
#Проверить, что при переключении валют цены на товары меняются в каталоге

@pytest.mark.parametrize("currency_from, currency_to", [("USD", "EUR"), ("EUR", "USD")])
@pytest.mark.parametrize("page_path", ["/", "/3-clothes"])
def test_currency_check(driver, wait, base_url, currency_to, currency_from, page_path):

    driver.get(base_url + page_path)

    # Получить валюту
    def switch_currency(currency_code):
        # Нажать на кнопку смены валюты
        currency_selector = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Currency dropdown']")))
        currency_selector.click()
        # Открылось окно выбора, выбрать нужную валюту
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'currency-selector')]//a[contains(text(),'{currency_code}')]")))
        option.click()

        wait.until(lambda d: all(currency_code in el.text for el in d.find_elements(By.CSS_SELECTOR, "div.current-price")))

    # Сменить валюту и проверить цены
    switch_currency(currency_from)
    prices_before = [el.text for el in driver.find_elements(By.CSS_SELECTOR, "div.current-price")]

    switch_currency(currency_to)
    prices_after = [el.text for el in driver.find_elements(By.CSS_SELECTOR, "div.current-price")]

    assert len(prices_before) == len(prices_after)

    for i,  (before, after) in zip(prices_before, prices_after):
        assert before != after
        f"Цена не изменилась для элемента #{i}: "
        f"было '{before}', стало '{after}' "
        f"(валюта {currency_from} → {currency_to})"
"""