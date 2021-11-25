import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.usefixtures('setup', 'website_setup')
class TestLoginPage:

    @allure.title('Login with invalid user test')
    @allure.description('This is test of login with invalid user')
    def test_login_failed(self, config):
        login_page = LoginPage(self.driver, config)
        login_page.open('account-center/signin-identifier.html')
        error_msg = '用户名称或密码不正确'
        assert error_msg in login_page.login_with_invalid_user('test')

    @allure.title('Login with valid user test')
    @allure.description('This is test of login with valid user')
    def test_login_passed(self, config):
        login_page = LoginPage(self.driver, config)
        login_page.open('account-center/signin-identifier.html')
        url_clip = 'cn/zh/home'
        assert url_clip in login_page.login_with_valid_user('boxing').get_url()
