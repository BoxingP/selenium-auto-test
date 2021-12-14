import allure
import pytest

from pages.main_page import MainPage


@pytest.mark.usefixtures('setup', 'website_setup')
class TestMainPage:

    @allure.title('Open login page test')
    @allure.description('This is test of open login page on main page')
    def test_login_page_opened(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open()
        main_page.go_to_login_page()
        link_clip = 'account-center/signin-identifie'
        assert link_clip in main_page.get_url()
