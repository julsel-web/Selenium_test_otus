import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--base-url", default="http://localhost:8081")


@pytest.fixture()
def base_url(request):
    return request.config.getoption("base_url")


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("headless")

    if browser_name == "ff":
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        service = FFService(executable_path="/snap/bin/geckodriver")
        browser = webdriver.Firefox(service=service, options=options)
    elif browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
    elif browser_name == "ya":
        service = ChromeService(
            executable_path="/Users/uliatuz/Downloads/drivers/yandexdriver"
        )
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.binary_location = "/Users/uliatuz/bin/yandex-browser"
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "safari":
        browser = webdriver.Safari()

    else:
        raise ValueError(f"Unknown browser: {browser_name}")

    yield browser

    browser.quit()
