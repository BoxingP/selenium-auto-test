import allure
import pytest

from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.locators import LoginPageLocators, MainPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestLoginPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @_step
    @allure.title('Login with invalid user test')
    @allure.description('This is test of login with invalid user')
    def test_login_with_invalid_user(self, config):
        login_page = MainPage(self.driver, config)
        login_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        login_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('test', is_valid=False)
        error_msg = '用户名称或密码不正确'
        assert error_msg in login_page.find_element(*LoginPageLocators.login_error_message).text

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @_step
    @allure.title('Login with valid user test')
    @allure.description('This is test of login with valid user')
    def test_login_with_valid_user(self, config):
        login_page = MainPage(self.driver, config)
        login_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        login_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('boxing', is_valid=True)
        profile_msg = '账户'
        assert profile_msg in login_page.find_element(*MainPageLocators.user_profile_menu).text
        login_page.logout()
