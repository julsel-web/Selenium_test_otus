import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 5)

def test_homepage_elements(driver, base_url, wait):
    driver.get(base_url)

    logo = wait.until(EC.visibility_of_element_located((By.ID, "_mobile_logo")))
    assert logo.is_displayed()

    menu = wait.until(EC.visibility_of_element_located((By.ID, "menu-icon")))
    assert menu.is_displayed()

    carousel = wait.until(EC.visibility_of_element_located((By.ID, "carousel")))
    assert carousel.is_displayed()

    cards = carousel.find_elements(By.TAG_NAME, "li")
    assert len(cards) > 0

    popular = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.products.row")))
    assert popular.is_displayed()

    popular_cards = popular.find_elements(By.CSS_SELECTOR, "div.js-product")
    assert len(popular_cards) > 0

    for i, card in enumerate(popular_cards, 1):
        assert card.is_displayed()

    footer = wait.until(EC.visibility_of_element_located((By.ID, "footer")))
    assert footer.is_displayed()



def test_catology_elements(driver, base_url, wait):
    driver.get(f"{base_url}/3-clothes")

    filtres = wait.until(EC.visibility_of_element_located((By.ID, "left-column")))
    assert filtres.is_displayed()

    category = wait.until(EC.visibility_of_element_located((By.ID, "subcategories")))
    assert category.is_displayed()

    sort_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".products-sort-order .btn-unstyle.select-title")))
    assert sort_button.is_displayed()

    sort_button.click()

    drop_menu = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".products-sort-order .dropdown-menu"))
    )
    assert drop_menu.is_displayed()

    options = drop_menu.find_elements(By.CSS_SELECTOR, "a.select-list")
    assert len(options) > 0

    filter_button = wait.until(
        EC.visibility_of_element_located((By.ID, "search_filter_toggler"))
    )
    assert filter_button.is_displayed()

    filter_button.click()

    filter_panel = wait.until(
        EC.visibility_of_element_located((By.ID, "search_filters_wrapper"))
    )
    assert filter_panel.is_displayed()

    filter_panel.find_element(By.CSS_SELECTOR, "button.btn.btn-secondary.ok").click()

    product = wait.until(EC.visibility_of_element_located((By.ID, "js-product-list")))
    assert product.is_displayed()

    btn_back = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".hidden-md-up.text-xs-right.up a.btn")))
    assert btn_back.is_displayed()

    btn_back.click()

    header = wait.until(EC.visibility_of_element_located((By.ID, "header")))
    assert header.is_displayed()



def test_product_card_elements(driver, base_url, wait):
    driver.get(f"{base_url}/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white")

    main_image = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.js-qv-product-cover.img-fluid")))
    assert main_image.is_displayed()

    title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.h1")))
    assert title.is_displayed()

    price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.current-price")))
    assert price.is_displayed()

    price_number = float(re.sub(r"[^\d.,]", "", price.text).replace(",", "."))
    assert price_number !=0

    description = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.product-description")))
    assert description.is_displayed()

    add_to_cart = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.add-to-cart")))
    assert add_to_cart.is_displayed()

    add_to_cart.click()

    product_card = wait.until(EC.visibility_of_element_located((By.ID, "blockcart-modal")))
    assert product_card.is_displayed()


def test_admin_elements(driver, base_url, wait):
    driver.get(f"{base_url}/administration")

    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    assert email_input.is_displayed()
    email_input.send_keys("jul.sel@findmykids.org")

    password_input = wait.until(EC.visibility_of_element_located((By.ID, "passwd")))
    assert password_input.is_displayed()
    password_input.send_keys("sdjcbsdkhbvc")

    login_button = wait.until(EC.visibility_of_element_located((By.ID, "submit_login")))
    assert login_button.is_displayed()

    login_button.click()

    error_msg = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger")))
    assert error_msg.is_displayed()

    #stay_logged_in = wait.until(EC.visibility_of_element_located((By.ID, "stay_logged_in")))
    #assert stay_logged_in.is_displayed()

    forgot_password_link = wait.until(EC.visibility_of_element_located((By.ID, "forgot-password-link")))
    assert forgot_password_link.is_displayed()

    forgot_password_link.click()

    rerequest_password_reset = wait.until(EC.visibility_of_element_located((By.ID, "forgot_password_form")))
    assert rerequest_password_reset.is_displayed()

def test_registr_elements(driver, base_url, wait):
        driver.get(f"{base_url}/registration")

        ft_input = wait.until(EC.visibility_of_element_located((By.ID, "field-firstname")))
        assert ft_input.is_displayed()

        ln_input = wait.until(EC.visibility_of_element_located((By.ID, "field-lastname")))
        assert ln_input.is_displayed()

        email_new_input = wait.until(EC.visibility_of_element_located((By.ID, "field-email")))
        assert email_new_input.is_displayed()

        password_new_input = wait.until(EC.visibility_of_element_located((By.ID, "field-password")))
        assert password_new_input.is_displayed()

        hb_input = wait.until(EC.visibility_of_element_located((By.ID, "field-birthday")))
        assert hb_input.is_displayed()

        save_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "footer.form-footer button.btn.btn-primary.form-control-submit")))
        assert save_button.is_displayed()










    

    





