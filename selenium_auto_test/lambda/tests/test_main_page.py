from pages.main_page import MainPage
from tests.test import Test


class TestMainPage(Test):

    def test_page_load(self):
        main_page = MainPage(self.driver)
        main_page.open()
        self.assertTrue(main_page.check_page_loaded())

    def test_sign_in_button(self):
        main_page = MainPage(self.driver)
        main_page.open()
        self.assertIn("account-center/signin-identifier", main_page.go_to_login_page().get_url())
