import allure
import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.locators import CartPageLocators, MainPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:

    @_step
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add forgotten product to cart test')
    @allure.description('This is test of add forgotten product to cart')
    def test_forgotten_product_added_to_cart(self, config, product):
        cart_page = CartPage(self.driver, config)
        cart_page.open_page(f"store/cart?cid={config['cid']}")
        cart_page.add_forgot_item(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        assert product['name'] in cart_page.find_element(*CartPageLocators.cart_item_name).text

    @_step
    @allure.title('Open quick order page test')
    @allure.description('This is test of open quick order page')
    def test_quick_order_page_opened(self, config):
        cart_page = CartPage(self.driver, config)
        cart_page.open_page(f"/store/quick-order?cid={config['cid']}")
        cart_page.quick_add_item(catalog_number='', quantity='1')
        cart_page.wait_element_to_be_visible(*CartPageLocators.fill_out_error_msg)
        error_msg = '没有已提供的产品信息'
        assert error_msg in cart_page.find_element(*CartPageLocators.fill_out_error_msg).text

    @_step
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Checkout order test')
    @allure.description('This is test of checkout order')
    def test_checkout_order(self, config, product):
        login_page = MainPage(self.driver, config)
        login_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        login_page.go_to_login_page()
        login_page.wait_url_changed_to('proxy.html')
        login_page.wait_url_changed_to('signin-identifier.html')
        login_page = LoginPage(self.driver, config)
        login_page.login('boxing')
        login_page.wait_url_changed_to('proxy.html')
        login_page.wait_url_changed_to('home.html')
        login_page.wait_element(*MainPageLocators.user_profile_menu)
        cart_page = CartPage(self.driver, config)
        cart_page.open_page(f"store/cart?cid={config['cid']}")
        cart_page.wait_element_to_be_clickable(*CartPageLocators.add_forgot_to_cart_button)
        cart_page.add_forgot_item(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        cart_page.submit_order(ship_to='test', bill_to='test', order_number='NA', is_submit=False)
        assert product['name'] in cart_page.find_element(*CartPageLocators.added_item_name_field).text
        cart_page.empty_cart()
