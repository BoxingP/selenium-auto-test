from pages.home_page import HomePage
from pages.page import Page
from utils.locators import LoginPageLocators
from utils.users import User


class LoginPage(Page):
    def __init__(self, driver):
        self.locator = LoginPageLocators
        super(LoginPage, self).__init__(driver)

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

    def login_with_invalid_user(self, user):
        self.login(user)
        self.wait_element(*self.locator.ERROR_LABEL)
        return self.find_element(*self.locator.ERROR_MESSAGE).text

    def login_with_valid_user(self, user):
        self.login(user)
        self.wait_element(*self.locator.CUSTOMER_NAME)
        return HomePage(self.driver)
