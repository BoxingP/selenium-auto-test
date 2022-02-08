import allure

from pages.page import Page
from utils.locators import CartPageLocators


class CartPage(Page):
    def __init__(self, driver, config):
        self.locator = CartPageLocators
        super(CartPage, self).__init__(driver, config)

    @allure.step('Add forgot item by catalog number: {catalog_number}')
    def add_forgot_item(self, catalog_number, quantity=None):
        self.input_text(catalog_number, *self.locator.forgot_item_catalog_number_field)
        if quantity is not None:
            self.input_text(quantity, *self.locator.forgot_item_quantity_field, is_overwrite=True)
        self.click(*self.locator.add_forgot_to_cart_button)

    def empty_cart(self):
        if self.is_element_exists(*self.locator.empty_cart_button):
            self.click(*self.locator.empty_cart_button)
            self.click(*self.locator.confirm_empty_cart_button)
