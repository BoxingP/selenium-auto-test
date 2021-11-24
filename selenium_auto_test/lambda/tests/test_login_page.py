from pages.login_page import LoginPage
from tests.test import Test


class TestLoginPage(Test):

    def test_sign_in_with_invalid_user(self):
        login_page = LoginPage(self.driver)
        self.driver.get('https://www.thermofisher.cn/account-center/signin-identifier.html')
        self.driver.implicitly_wait(10)
        result = login_page.login_with_invalid_user('test')
        self.assertIn('用户名称或密码不正确', result)

    def test_sign_in_with_valid_user(self):
        login_page = LoginPage(self.driver)
        self.driver.get('https://www.thermofisher.cn/account-center/signin-identifier.html')
        self.driver.implicitly_wait(10)
        result = login_page.login_with_valid_user('boxing')
        self.driver.implicitly_wait(10)
        self.assertIn('cn/zh/home', result.get_url())
