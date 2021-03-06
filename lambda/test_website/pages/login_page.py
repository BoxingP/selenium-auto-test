import allure

from pages.page import Page
from utils.locators import LoginPageLocators, HomePageLocators
from utils.logger import _step
from utils.users import User


class LoginPage(Page):
    def __init__(self, driver, config):
        super(LoginPage, self).__init__(driver, config)
        self.locator = LoginPageLocators

    @_step
    @allure.step('Login with user: {user}')
    def login(self, user, is_valid, save_cookie=False):
        user = User().get_user(user)
        self.input_text(user['email'], *self.locator.username_field)
        self.click(*self.locator.next_button)
        self.input_text(user['password'], *self.locator.password_field)
        self.click(*self.locator.sign_in_button)
        if is_valid:
            self.wait_url_changed_to('proxy.html')
            self.wait_url_changed_to('home.html')
            self.wait_element(*HomePageLocators.user_profile_menu)
            if save_cookie:
                self.save_cookie(user['name'])
        else:
            self.wait_element(*self.locator.login_error)

    @_step
    @allure.step('Logout')
    def logout(self):
        self.hover(*HomePageLocators.user_profile_menu)
        self.click(*HomePageLocators.sign_out_link)
        self.wait_element(*HomePageLocators.logo_image)
