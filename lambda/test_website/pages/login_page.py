from pages.page import Page
from utils.locators import LoginPageLocators, MainPageLocators
from utils.users import User


class LoginPage(Page):
    def __init__(self, driver, config):
        self.locator = LoginPageLocators
        super(LoginPage, self).__init__(driver, config)

    def enter_email(self, email):
        self.wait_element_to_be_clickable(*self.locator.EMAIL)
        self.find_element(*self.locator.EMAIL).send_keys(email)

    def click_next_button(self):
        self.find_element(*self.locator.NEXT).click()

    def enter_password(self, password):
        self.wait_element_to_be_clickable(*self.locator.PASSWORD)
        self.find_element(*self.locator.PASSWORD).send_keys(password)

    def click_login_button(self):
        self.wait_element_to_be_clickable(*self.locator.SUBMIT)
        self.find_element(*self.locator.SUBMIT).click()

    def login(self, user):
        user = User().get_user(user)
        self.enter_email(user['email'])
        self.click_next_button()
        self.enter_password(user['password'])
        self.click_login_button()

    def logout(self):
        self.hover(*MainPageLocators.PROFILE_ENTRY)
        self.find_element(*MainPageLocators.SIGN_OUT).click()
        self.wait_element(*MainPageLocators.LOGO)
