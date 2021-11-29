import os

import pytest
import yaml

from utils.driver_factory import DriverFactory

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
DEFAULT_WAIT_TIME = 10
DEFAULT_WEBSITE = 'https://www.baidu.com/'
SUPPORTED_BROWSERS = ['chrome']


@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


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


@pytest.fixture()
def setup(request, config):
    driver = DriverFactory.get_driver(config['browser'], config['headless_mode'])
    driver.implicitly_wait(config['timeout'])
    request.cls.driver = driver
    yield
    driver.quit()
