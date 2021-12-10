import allure
import pytest

from pages.login_page import LoginPage
from utils.locators import LoginPageLocators, MainPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestLoginPage:

    @allure.title('Login with invalid user test')
    @allure.description('This is test of login with invalid user')
    def test_login_failed(self, config):
        login_page = LoginPage(self.driver, config)
        login_page.open('account-center/signin-identifier.html')
        login_page.login('test')
        error_msg = '用户名称或密码不正确'
        login_page.wait_element(*LoginPageLocators.ERROR_LABEL)
        assert error_msg in login_page.find_element(*LoginPageLocators.ERROR_MESSAGE).text

    @allure.title('Login with valid user test')
    @allure.description('This is test of login with valid user')
    def test_login_passed(self, config):
        login_page = LoginPage(self.driver, config)
        login_page.open('account-center/signin-identifier.html')
        login_page.login('boxing')
        profile_msg = '账户'
        login_page.wait_element(*MainPageLocators.PROFILE_ENTRY)
        assert profile_msg in login_page.find_element(*MainPageLocators.PROFILE_ENTRY).text
        login_page.logout()
