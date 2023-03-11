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

    @_step
    @allure.step('Go to cart page')
    def go_to_cart_page(self):
        self.click(*self.locator.cart_menu)
        self.click(*self.locator.view_cart_button)
        self.wait_url_changed_to('cart')

    @_step
    @allure.step('Open login page')
    def go_to_login_page(self):
        self.click(*self.locator.sign_in_menu)
        self.click(*self.locator.sign_in_button)
        self.wait_url_changed_to('proxy.html')
        self.wait_url_changed_to('signin-identifier.html')

    @_step
    @allure.step('Open registration page')
    def go_to_registration_page(self):
        self.click(*self.locator.sign_in_menu)
        self.click(*self.locator.registration_link)
        self.wait_url_changed_to('registration')

    @_step
    @allure.step('Open account page')
    def go_to_account_page(self):
        self.click(*HomePageLocators.logged_in_menu)
        self.click(*self.locator.account_link)
        self.wait_url_changed_to('accounts')

    @_step
    @allure.step('Search product')
    def search_product(self, words):
        self.input_text(words, *self.locator.search_product_field)
        self.click(*self.locator.search_product_button)
        self.wait_element_to_be_visible(*self.locator.search_product_result)

    @_step
    @allure.step('Check header banner exists')
    def check_header_banner_exists(self):
        if self.is_element_exists(*self.locator.header_banner) \
                and self.is_element_clickable(*self.locator.header_banner):
            return True
        else:
            return False

    @_step
    @allure.step('Check top banner exists')
    def check_top_banner_exists(self):
        self.wait_element_to_be_visible(*self.locator.top_banner)
        return True if self.is_element_exists(*self.locator.top_banner) else False

    @_step
    @allure.step('Open online chat')
    def open_online_chat(self):
        self.wait_element_to_be_visible(*self.locator.online_chat_button)
        self.click(*self.locator.online_chat_button)
        self.wait_frame_to_be_visible(*self.locator.online_chat_frame)
        self.wait_element_to_be_visible(*self.locator.online_chat_title)
