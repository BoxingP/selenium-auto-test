import allure
import pytest

from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestAccountPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check order history exists test')
    @allure.description('This is test of check order history exists on account page')
    def test_order_history_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        main_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('history', is_valid=True)
        main_page.go_to_account_page()
        account_page = AccountPage(self.driver, config)
        account_page.go_to_order_history_page()
        assert account_page.check_order_history_exists()
