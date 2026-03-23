import pytest
import uuid

from page_object.main_page import MainPage
from page_object.elements.login_form import LoginForm
from page_object.cart_page import CartPage
from page_object.product_page import ProductPage
from page_object.checkout_page import CheckoutPage
from page_object.elements.registr_form import ReristForm
from page_object.catalog_admin_page import CatalogAdminPage


def test_admin_login_logout(driver, base_url):
    driver.get(f"{base_url}/administration")
    LoginForm(driver).login("admin@example.com","Admin123!")
    CheckoutPage(driver).checkout_admin_page()
    LoginForm(driver).logout()
    CheckoutPage(driver).checkout_login_page()

def test_add_card(driver, base_url):

    driver.get(f"{base_url}/administration")
    LoginForm(driver).login("admin@example.com","Admin123!")
    CatalogAdminPage(driver).catalog_page()
    CatalogAdminPage(driver).products_page()
    CatalogAdminPage(driver).add_new_products("combinations", "NEW TEST CARD")
    CheckoutPage(driver).checkout_add_new_card("NEW TEST CARD")

def test_delete_card(driver, base_url):

    driver.get(f"{base_url}/administration")
    LoginForm(driver).login("admin@example.com","Admin123!")
    CatalogAdminPage(driver).catalog_page()
    CatalogAdminPage(driver).products_page()
    name = CatalogAdminPage(driver).delete_products("NEW TEST CARD")
    CheckoutPage(driver).checkout_delete_product("NEW TEST CARD")






#Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине

def test_homepage_elements(driver, base_url):
    driver.get(base_url)
    product_href = MainPage(driver).choose_random_product_and_get_href()
    ProductPage(driver).add_to_cart()
    ProductPage(driver).click_to_cart()
    product_cat = CartPage(driver).check_card_to_cart()
    cart_href = product_cat.get_attribute("href")
    assert cart_href  == product_href



#Проверить, что при переключении валют цены на товары меняются на главной
#Проверить, что при переключении валют цены на товары меняются в каталоге

@pytest.mark.parametrize("currency_from, currency_to", [("USD", "EUR"), ("EUR", "USD")])
@pytest.mark.parametrize("page_path", ["/", "/3-clothes"])
def test_currency_check(driver,base_url, currency_to, currency_from, page_path):
    driver.get(base_url + page_path)
    prices_before = MainPage(driver).switch_currency(currency_from)
    prices_after = MainPage(driver).switch_currency(currency_to)
    assert len(prices_before) == len(prices_after)
    for i,  (before, after) in enumerate(zip(prices_before, prices_after)):
        assert before != after
        f"Цена не изменилась для элемента #{i}: "
        f"было '{before}', стало '{after}' "
        f"(валюта {currency_from} → {currency_to})"

def test_regictration(driver, base_url):
    driver.get(f"{base_url}/registration")
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    ReristForm(driver).registr("Mrs","Julia","Tuz", email,
                               "nF#K[pvT<7P[(Fo", "08/09/1997")
    CheckoutPage(driver).checkout_my_account()

