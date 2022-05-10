import allure

from pages.page import Page
from utils.locators import LoginPageLocators, MainPageLocators
from utils.logger import _step
from utils.users import User


class LoginPage(Page):
    def __init__(self, driver, config):
        self.locator = LoginPageLocators
        super(LoginPage, self).__init__(driver, config)

    @_step
    @allure.step('Login with user: {user}')
    def login(self, user):
        user = User().get_user(user)
        self.input_text(user['email'], *self.locator.username_field)
        self.click(*self.locator.next_button)
        self.input_text(user['password'], *self.locator.password_field)
        self.click(*self.locator.sign_in_button)

    @_step
    @allure.step('Logout')
    def logout(self):
        self.hover(*MainPageLocators.user_profile_menu)
        self.click(*MainPageLocators.sign_out_link)
        self.wait_element(*MainPageLocators.logo_image)
