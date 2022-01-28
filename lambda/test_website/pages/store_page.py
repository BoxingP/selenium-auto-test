import allure
from selenium.webdriver.common.keys import Keys

from pages.page import Page
from utils.locators import StorePageLocators


class StorePage(Page):
    def __init__(self, driver, config):
        self.locator = StorePageLocators
        super(StorePage, self).__init__(driver, config)

    @allure.step('Add forgot item by catalog number: {catalog_number}')
    def add_forgot_item(self, catalog_number, quantity=None):
        self.input_text(catalog_number, *self.locator.forgot_item_catalog_number_field)
        if quantity is not None:
            self.input_text(Keys.CONTROL + 'a', *self.locator.forgot_item_quantity_field)
            self.input_text(Keys.DELETE, *self.locator.forgot_item_quantity_field)
            self.input_text(quantity, *self.locator.forgot_item_quantity_field)
        self.click(*self.locator.add_forgot_to_cart_button)

    def add_product(self, catalog_number, quantity):
        self.open('order/catalog/product/{}'.format(catalog_number))
        self.input_text(quantity, *self.locator.product_quantity_field)
        self.click(*self.locator.add_product_to_cart_button)
        self.wait_element_to_be_visible(*self.locator.cart_info)
        self.click(*self.locator.view_cart)
        self.wait_element_to_be_visible(*self.locator.order_summary)
