import json
import os

import pytest

from utils.driver_factory import DriverFactory
from utils.json_report import JSONReport
from utils.screenshot import Screenshot

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
DEFAULT_WEBSITE = 'https://www.baidu.com/'


@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        return json.load(file)


@pytest.fixture(scope='session')
def website_setup(config):
    return config['base_url'] if 'base_url' in config else DEFAULT_WEBSITE


@pytest.fixture(scope='session')
def product():
    path = os.path.join(os.path.dirname(__file__), 'product.json')
    with open(path, 'r', encoding='UTF-8') as file:
        product = json.load(file)
    return product


@pytest.fixture(scope='class')
def setup(request, config):
    driver = DriverFactory.get_driver(config['browser'], config['headless_mode'])
    driver.implicitly_wait(config['timeout'])
    request.cls.driver = driver
    yield request.cls.driver
    request.cls.driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='function', autouse=True)
def screenshot_on_failure(request, config):
    yield
    if request.node.rep_setup.passed and request.node.rep_call.failed:
        current_test = request.node.name.split(':')[-1].split(' ')[0].lower()
        driver = request.cls.driver
        Screenshot.take_screenshot(driver, config, 'test call failed', test=current_test)


def pytest_addoption(parser):
    parser.addoption(
        '--json', action='store', dest='json_path', default=None, help='where to store the json report'
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    json_path = config.option.json_path
    config.pluginmanager.register(JSONReport(json_path), name='json_report')
