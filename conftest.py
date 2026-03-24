import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions


SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

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

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_name = f"{request.node.name}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
        try:
            browser.save_screenshot(screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Screenshot_{request.node.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            print(f"Скриншот сохранен: {screenshot_path}")
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")

    browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
