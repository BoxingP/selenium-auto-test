import allure

from pages.page import Page
from utils.locators import HomePageLocators


class HomePage(Page):
    def __init__(self, driver, config):
        self.locator = HomePageLocators
        super(HomePage, self).__init__(driver, config)

    @allure.step('Open home page')
    def check_page_loaded(self):
        return True if self.find_element(*self.locator.logo_image) else False
