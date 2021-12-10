import allure

from pages.page import Page
from utils.locators import MainPageLocators


class MainPage(Page):
    def __init__(self, driver, config):
        self.locator = MainPageLocators
        super(MainPage, self).__init__(driver, config)

    @allure.step('Open main page')
    def check_page_loaded(self):
        return True if self.find_element(*self.locator.logo_image) else False

    @allure.step('Open login page')
    def go_to_login_page(self):
        self.hover(*self.locator.my_account_menu)
        self.click(*self.locator.sign_in_link)
        self.wait_element(*self.locator.logo_image)
