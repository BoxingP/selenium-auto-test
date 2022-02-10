import allure

from pages.page import Page
from utils.locators import ProductPageLocators


class ProductPage(Page):
    def __init__(self, driver, config):
        self.locator = ProductPageLocators
        super(ProductPage, self).__init__(driver, config)

    @allure.step('Add product by catalog number: {catalog_number}')
    def add_product(self, catalog_number, quantity):
        self.open('order/catalog/product/{}'.format(catalog_number))
        self.wait_element_to_be_clickable(*self.locator.save_to_list_button)
        self.input_text('9999', *self.locator.product_quantity_field, is_overwrite=True)
        retry = 0
        while self.find_element(*self.locator.product_quantity_field).get_attribute("value") != '':
            if retry > 5:
                break
            self.input_text(quantity, *self.locator.product_quantity_field, is_overwrite=True)
            self.click(*self.locator.add_to_cart_button)
            retry += 1
