import json
import os

import allure
import pytest
from allure_commons.types import AttachmentType

from utils.driver_factory import DriverFactory

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
DEFAULT_WAIT_TIME = 10
DEFAULT_WEBSITE = 'https://www.baidu.com/'
SUPPORTED_BROWSERS = ['chrome']


@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        return json.load(file)


@pytest.fixture(scope='session')
def browser_setup(config):
    if 'browser' not in config:
        raise Exception('The config file does not contain "browser"')
    elif config['browser'] not in SUPPORTED_BROWSERS:
        raise Exception(f'"{config["browser"]}" is not a supported browser')
    return config['browser']


@pytest.fixture(scope='session')
def wait_time_setup(config):
    return config['wait_time'] if 'wait_time' in config else DEFAULT_WAIT_TIME


@pytest.fixture(scope='session')
def website_setup(config):
    return config['tested_page'] if 'tested_page' in config else DEFAULT_WEBSITE


@pytest.fixture(scope='session')
def product():
    path = os.path.join(os.path.dirname(__file__), 'product.json')
    with open(path, 'r', encoding='UTF-8') as file:
        product = json.load(file)
    return product


@pytest.fixture()
def setup(request, config):
    driver = DriverFactory.get_driver(config['browser'], config['headless_mode'])
    driver.implicitly_wait(config['timeout'])
    request.cls.driver = driver
    before_failed = request.session.testsfailed
    yield
    if request.session.testsfailed != before_failed:
        allure.attach(driver.get_screenshot_as_png(), name="Test failed", attachment_type=AttachmentType.PNG)
    driver.quit()


@pytest.mark.tryfirst
def pytest_configure(config):
    config.pluginmanager.register(NumberOfFailed(), 'number_of_failed')


class NumberOfFailed(object):
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when != 'call':
            return
        if report.passed:
            self.passed += 1
        elif report.failed:
            self.failed += 1

    def pytest_sessionfinish(self, session, exitstatus):
        print(self.failed)
