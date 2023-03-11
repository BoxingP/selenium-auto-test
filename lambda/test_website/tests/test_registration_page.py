import allure
import pytest

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.locators import RegistrationPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestRegistrationPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Register with existing user test')
    @allure.description('This is test of register with existing user')
    def test_register_with_existing_user(self, config):
        registration_page = HomePage(self.driver, config)
        registration_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        registration_page.go_to_registration_page()
        registration_page = RegistrationPage(self.driver, config)
        registration_page.register('boxing', is_exist=True)
        error_msg = '该邮箱地址已注册'
        assert error_msg in registration_page.find_element(*RegistrationPageLocators.registration_error_message).text
