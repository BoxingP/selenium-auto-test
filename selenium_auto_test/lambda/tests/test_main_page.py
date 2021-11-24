from pages.main_page import MainPage
from tests.test import Test


class TestMainPage(Test):

    def test_page_load(self):
        page = MainPage(self.driver)
        self.driver.get('https://www.thermofisher.cn/')
        self.assertTrue(page.check_page_loaded())

    def test_sign_in_button(self):
        page = MainPage(self.driver)
        self.driver.get('https://www.thermofisher.cn/')
        self.assertIn("account-center/signin-identifier", page.go_to_login_page().get_url())
