from selenium.webdriver import ActionChains

from pages.login_page import LoginPage
from pages.page import Page
from utils.locators import MainPageLocators


class MainPage(Page):
    def __init__(self, driver):
        self.locator = MainPageLocators
        super(MainPage, self).__init__(driver)

    def check_page_loaded(self):
        return True if self.find_element(*self.locator.LOGO) else False

    def go_to_login_page(self):
        account_element = self.find_element(*self.locator.ACCOUNT)
        sign_in_element = self.find_element(*self.locator.SIGN_IN)
        hover = ActionChains(self.driver).move_to_element(account_element).move_to_element(sign_in_element)
        hover.click(sign_in_element)
        hover.perform()
        self.wait_element(*self.locator.LOGO)
        return LoginPage(self.driver)
