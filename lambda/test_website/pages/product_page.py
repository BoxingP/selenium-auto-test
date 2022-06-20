import allure

from pages.page import Page
from utils.locators import ProductPageLocators, CartPageLocators
from utils.logger import _step


class ProductPage(Page):
    def __init__(self, driver, config):
        super(ProductPage, self).__init__(driver, config)
        self.locator = ProductPageLocators

    @_step
    @allure.step('Add product by catalog number: {catalog_number}')
    def add_product(self, catalog_number, product_name, quantity):
        self.wait_element_to_be_clickable(*self.locator.save_to_list_button)
        self.input_text('9999', *self.locator.product_quantity_field, is_overwrite=True)
        retry = 0
        while self.find_element(*self.locator.product_quantity_field).get_attribute("value") != '':
            if retry > 5:
                break
            self.input_text(quantity, *self.locator.product_quantity_field, is_overwrite=True)
            self.click(*self.locator.add_to_cart_button)
            retry += 1
        self.wait_text_to_be_display(product_name, *self.locator.added_product_info)

    @_step
    @allure.step('Go to cart page')
    def go_to_cart_page(self):
        self.click(*self.locator.view_cart_button)
        self.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
