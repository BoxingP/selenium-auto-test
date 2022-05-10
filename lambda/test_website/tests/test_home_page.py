import allure
import pytest

from pages.home_page import HomePage
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestHomePage:

    @_step
    @allure.title('Open home page test')
    @allure.description('This is test of open home page')
    def test_page_loaded(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        assert home_page.check_page_loaded()
