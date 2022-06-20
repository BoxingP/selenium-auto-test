import allure

from pages.page import Page
from utils.locators import MainPageLocators
from utils.logger import _step


class MainPage(Page):
    def __init__(self, driver, config):
        super(MainPage, self).__init__(driver, config)
        self.locator = MainPageLocators

    @_step
    @allure.step('Go to cart page')
    def go_to_cart_page(self):
        self.click(*self.locator.my_cart)
        self.wait_url_changed_to('cart')

    @_step
    @allure.step('Open login page')
    def go_to_login_page(self):
        self.hover(*self.locator.my_account_menu)
        self.click(*self.locator.sign_in_link)
        self.wait_url_changed_to('proxy.html')
        self.wait_url_changed_to('signin-identifier.html')

    @_step
    @allure.step('Open registration page')
    def go_to_registration_page(self):
        self.hover(*self.locator.my_account_menu)
        self.click(*self.locator.registration_link)
        self.wait_url_changed_to('registration')

    @_step
    @allure.step('Open account page')
    def go_to_account_page(self):
        self.hover(*self.locator.user_profile_menu)
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
    @allure.step('Check yellow thin banner exists')
    def check_yellow_thin_banner_exists(self):
        if self.is_element_exists(*self.locator.yellow_thin_banner) \
                and self.is_element_clickable(*self.locator.yellow_thin_banner):
            return True
        else:
            return False

    @_step
    @allure.step('Check top banner exists')
    def check_top_banner_exists(self):
        self.wait_element_to_be_visible(*self.locator.top_banner)
        return True if self.is_element_exists(*self.locator.top_banner) else False

    @_step
    @allure.step('Check landscape banner exists')
    def check_landscape_banner_exists(self):
        self.scroll_page(direction='down')
        if self.is_element_exists(*self.locator.landscape_banner) \
                and self.is_element_clickable(*self.locator.landscape_banner):
            return True
        else:
            return False

    @_step
    @allure.step('Check order index exists')
    def check_order_index_exists(self):
        if self.find_element(*self.locator.order_index_img).is_displayed() \
                and self.is_element_clickable(*self.locator.order_index_img):
            return True
        else:
            return False
