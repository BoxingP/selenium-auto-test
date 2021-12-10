from pages.page import Page
from utils.locators import MainPageLocators


class MainPage(Page):
    def __init__(self, driver, config):
        self.locator = MainPageLocators
        super(MainPage, self).__init__(driver, config)

    def check_page_loaded(self):
        return True if self.find_element(*self.locator.LOGO) else False

    def go_to_login_page(self):
        self.hover(*self.locator.ACCOUNT)
        self.find_element(*self.locator.SIGN_IN).click()
        self.wait_element(*self.locator.LOGO)
