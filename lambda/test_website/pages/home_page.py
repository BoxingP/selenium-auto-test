import allure

from pages.page import Page
from utils.locators import HomePageLocators
from utils.logger import _step


class HomePage(Page):
    def __init__(self, driver, config):
        super(HomePage, self).__init__(driver, config)
        self.locator = HomePageLocators

    @_step
    @allure.step('Check home page whether loaded')
    def check_page_loaded(self):
        return True if self.find_element(*self.locator.logo_image) else False
