import pytest
import allure
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from page_object.base_page import BasePage


SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Браузер: chrome или ff")
    parser.addoption("--headless", action="store_true", help="Запуск браузера в headless")
    parser.addoption("--base-url", default="http://host.docker.internal:8081", help="Базовый URL сайта")
    parser.addoption("--remote", action="store_true", help="Использовать Selenoid")
    parser.addoption("--remote-url", default="http://selenoid:4444/wd/hub", help="URL Selenoid RemoteWebDriver")


@pytest.fixture()
def base_url(request):
    return request.config.getoption("base_url")


@pytest.fixture
def page(driver, base_url):
    return BasePage(driver, base_url)


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("headless")
    is_remote = request.config.getoption("remote")
    remote_url = request.config.getoption("remote_url")

    if is_remote:

        for _ in range(10):
            try:
                resp = requests.get(remote_url.replace("/wd/hub", "/status"), timeout=3)
                resp.raise_for_status()
                break
            except Exception:
                print("Ждём Selenoid...")
                time.sleep(2)
        else:
            raise RuntimeError(f"Selenoid недоступен по {remote_url}")

        browser_version = "120.0" if browser_name == "chrome" else "119.0"

        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
        elif browser_name == "ff":
            options = FFOptions()
            if headless:
                options.add_argument("--headless")
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")


        capabilities = options.to_capabilities()
        capabilities.update({
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "name": request.node.name
            }
        })

        browser = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=capabilities
        )

    else:

        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            from selenium.webdriver.chrome.service import Service as ChromeService
            service = ChromeService("/usr/bin/chromedriver")
            browser = webdriver.Chrome(service=service, options=options)

        elif browser_name == "ff":
            options = FFOptions()
            if headless:
                options.add_argument("--headless")
            from selenium.webdriver.firefox.service import Service as FFService
            service = FFService()
            browser = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

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
            print(f"Ошибка скриншота: {e}")


    if is_remote:
        try:
            video_url = f"{remote_url.replace('/wd/hub','')}/video/{browser.session_id}.mp4"
            allure.attach(video_url, name=f"Video_{request.node.name}", attachment_type=allure.attachment_type.MP4)
        except Exception as e:
            print(f"Не удалось прикрепить видео: {e}")

    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
