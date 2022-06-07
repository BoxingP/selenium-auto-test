from time import sleep

import allure

from pages.page import Page
from utils.locators import CartPageLocators
from utils.logger import _step


class CartPage(Page):
    def __init__(self, driver, config):
        self.locator = CartPageLocators
        super(CartPage, self).__init__(driver, config)

    @_step
    @allure.step('Add forgot item by catalog number: {catalog_number}')
    def add_forgot_item(self, catalog_number, quantity=None):
        self.input_text(catalog_number, *self.locator.forgot_item_catalog_number_field)
        if quantity is not None:
            self.input_text(quantity, *self.locator.forgot_item_quantity_field, is_overwrite=True)
        self.click(*self.locator.add_forgot_to_cart_button)
        self.wait_element_to_be_clickable(*self.locator.empty_cart_button)

    @_step
    @allure.step('Empty cart')
    def empty_cart(self):
        if self.is_element_exists(*self.locator.empty_cart_button):
            self.click(*self.locator.empty_cart_button)
            self.click(*self.locator.confirm_empty_cart_button)
            self.wait_element_to_be_visible(*self.locator.cart_emptied_msg)

    @_step
    @allure.step('Quick add items')
    def quick_add_item(self, catalog_number, quantity):
        self.input_text(catalog_number, *self.locator.quick_add_catalog_number_field)
        self.input_text(quantity, *self.locator.quick_add_quantity_field, is_overwrite=True)
        self.click(*self.locator.quick_add_product_to_cart_button)

    @_step
    @allure.step('Go to order details page')
    def go_to_order_details_page(self):
        self.click(*self.locator.checkout_button)
        self.wait_url_changed_to('orderEntry')

    @_step
    @allure.step('Fill order entries')
    def fill_order_entry(self, ship_to, bill_to, order_number):
        while not self.is_element_clickable(*self.locator.continue_button):
            self.input_text(ship_to, *self.locator.ship_recipient, is_overwrite=True)
            self.input_text(bill_to, *self.locator.bill_recipient, is_overwrite=True)
            self.input_text(order_number, *self.locator.purchase_order_number, is_overwrite=True)
            sleep(0.5)

    @_step
    @allure.step('Go to review and submit page')
    def go_to_review_submit_page(self):
        self.click(*self.locator.continue_button)
        self.wait_url_changed_to('reviewAndSubmit')
        self.wait_element_to_be_visible(*self.locator.order_summary_msg)

    @_step
    @allure.step('Submit order')
    def submit_order(self, is_submit):
        if is_submit:
            self.click(*self.locator.terms_conditions_accept_button)
            self.click(*self.locator.submit_order_button)
        else:
            self.click(*self.locator.back_to_cart_button)
            self.wait_url_changed_to('cart')
