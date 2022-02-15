import allure
import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from utils.locators import CartPageLocators, MainPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add forgotten product to cart test')
    @allure.description('This is test of add forgotten product to cart')
    def test_forgotten_product_added_to_cart(self, config, product):
        cart_page = CartPage(self.driver, config)
        cart_page.open('store/cart')
        cart_page.add_forgot_item(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        assert product['name'] in cart_page.find_element(*CartPageLocators.cart_item_name).text

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Checkout order test')
    @allure.description('This is test of checkout order')
    def test_checkout_order(self, config, product):
        login_page = LoginPage(self.driver, config)
        login_page.open('account-center/signin-identifier.html')
        login_page.login('boxing')
        login_page.wait_element(*MainPageLocators.user_profile_menu)
        cart_page = CartPage(self.driver, config)
        cart_page.open('store/cart')
        cart_page.empty_cart()
        cart_page.wait_element_to_be_visible(*CartPageLocators.cart_emptied_msg)
        cart_page.add_forgot_item(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        cart_page.click(*CartPageLocators.checkout_button)
        cart_page.input_text('test', *CartPageLocators.ship_recipient)
        cart_page.input_text('test', *CartPageLocators.bill_recipient)
        cart_page.input_text('NA', *CartPageLocators.purchase_order_number, is_overwrite=True)
        cart_page.click(*CartPageLocators.continue_button)
        cart_page.wait_element_to_be_visible(*CartPageLocators.order_summary_msg)
        assert product['quantity'] in cart_page.find_element(*CartPageLocators.product_items_info).text
        cart_page.click(*CartPageLocators.back_to_cart_button)
        cart_page.empty_cart()
