import json
import os

import allure
import pytest
from allure_commons.types import AttachmentType

from utils.driver_factory import DriverFactory
from utils.json_report import JSONReport

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
DEFAULT_WEBSITE = 'https://www.baidu.com/'


@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        return json.load(file)


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


def pytest_addoption(parser):
    parser.addoption(
        '--json', action='store', dest='json_path', default=None, help='where to store the json report'
    )


@pytest.mark.tryfirst
def pytest_configure(config):
    json_path = config.option.json_path
    config.pluginmanager.register(JSONReport(json_path), name='json_report')
