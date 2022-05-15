import allure

from pages.page import Page
from utils.locators import MainPageLocators
from utils.logger import _step


class MainPage(Page):
    def __init__(self, driver, config):
        self.locator = MainPageLocators
        super(MainPage, self).__init__(driver, config)

    @_step
    @allure.step('Open login page')
    def go_to_login_page(self):
        self.hover(*self.locator.my_account_menu)
        self.click(*self.locator.sign_in_link)
        self.wait_url_changed_to('proxy.html')
        self.wait_url_changed_to('signin-identifier.html')

    @_step
    @allure.step('Search product')
    def search_product(self, words):
        self.input_text(words, *self.locator.search_product_field)
        self.click(*self.locator.search_product_button)
        self.wait_element_to_be_visible(*self.locator.search_product_result)
