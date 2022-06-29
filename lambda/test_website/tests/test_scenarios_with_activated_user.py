import allure
import pytest

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
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
        username = 'history'
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        if not home_page.load_cookie(username):
            home_page.go_to_login_page()
            login_page = LoginPage(self.driver, config)
            login_page.login(username, is_valid=True, save_cookie=True)
        home_page.go_to_account_page()
        account_page = AccountPage(self.driver, config)
        account_page.go_to_order_history_page()
        assert account_page.check_order_history_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check shipping and billing addresses exist test')
    @allure.description('This is test of check shipping and billing addresses exist on account page')
    def test_shipping_billing_addresses_exist(self, config):
        username = 'history'
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        if not home_page.load_cookie(username):
            home_page.go_to_login_page()
            login_page = LoginPage(self.driver, config)
            login_page.login(username, is_valid=True, save_cookie=True)
        home_page.go_to_account_page()
        account_page = AccountPage(self.driver, config)
        account_page.go_to_personal_profile_page()
        assert account_page.check_shipping_address_exists(username) and \
               account_page.check_billing_address_exists(username)
