import pytest
import uuid

from page_object.main_page import MainPage
from page_object.login_form import LoginForm
from page_object.cart_page import CartPage
from page_object.product_page import ProductPage
from page_object.checkout_page import AssertionHelper
from page_object.catalog_admin_page import CatalogAdminPage
from page_object.base_page import BasePage
from page_object.elements.registr_form import RegistrationForm


def test_admin_login_logout(page: BasePage):
    page.open("/administration")
    LoginForm(page).login("admin@example.com","Admin123!")
    AssertionHelper(page).checkout_admin_page()
    LoginForm(page).logout()
    AssertionHelper(page).checkout_login_page()

def test_add_card(page: BasePage):
    page.open("/administration")
    LoginForm(page).login("admin@example.com","Admin123!")
    CatalogAdminPage(page).catalog_page()
    CatalogAdminPage(page).products_page()
    CatalogAdminPage(page).add_new_products("combinations", "NEW TEST CARD")
    AssertionHelper(page).checkout_add_new_card("NEW TEST CARD")

def test_delete_card(page: BasePage):
    page.open("/administration")
    LoginForm(page).login("admin@example.com","Admin123!")
    CatalogAdminPage(page).catalog_page()
    CatalogAdminPage(page).products_page()
    name = CatalogAdminPage(page).delete_products("NEW TEST CARD")
    AssertionHelper(page).checkout_delete_product(name)

#Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине

def test_homepage_elements(page: BasePage):
    page.open("/")
    product_href = MainPage(page).choose_random_product_and_get_href()
    ProductPage(page).add_to_cart()
    ProductPage(page).click_to_cart()
    product_cat = CartPage(page).check_card_to_cart()
    cart_href = product_cat.get_attribute("href")
    assert cart_href  == product_href



#Проверить, что при переключении валют цены на товары меняются на главной
#Проверить, что при переключении валют цены на товары меняются в каталоге

@pytest.mark.parametrize("currency_from, currency_to", [("USD", "EUR"), ("EUR", "USD")])
@pytest.mark.parametrize("page_path", ["/", "/3-clothes"])
def test_currency_check(page: BasePage, currency_to, currency_from, page_path):
    page.open(page_path)
    prices_before = MainPage(page).switch_currency(currency_from)
    prices_after = MainPage(page).switch_currency(currency_to)
    assert len(prices_before) == len(prices_after)
    for i,  (before, after) in enumerate(zip(prices_before, prices_after)):
        assert before != after, (
    f"Цена не изменилась для элемента #{i}: "
    f"было '{before}', стало '{after}' "
    f"(валюта {currency_from} → {currency_to})"
    )

def test_registration(page: BasePage):
    page.open("/registration")
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    RegistrationForm(page).registration("Mrs","Julia","Tuz", email,
                               "nF#K[pvT<7P[(Fo", "08/09/1997")
    AssertionHelper(page).checkout_my_account()

