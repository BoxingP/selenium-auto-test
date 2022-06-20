import allure
import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.locators import CartPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Add forgotten product to cart test')
    @allure.description('This is test of add forgotten product to cart')
    def test_forgotten_product_added_to_cart(self, config, product):
        cart_page = CartPage(self.driver, config)
        cart_page.open_page(f"store/cart?cid={config['cid']}")
        cart_page.add_forgot_item_to_cart(catalog_number=product['sku'], quantity=product['quantity'])
        assert product['name'] in cart_page.find_element(*CartPageLocators.cart_item_name).text

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Open quick order page test')
    @allure.description('This is test of open quick order page')
    def test_quick_order_product(self, config):
        cart_page = CartPage(self.driver, config)
        cart_page.open_page(f"/store/quick-order?cid={config['cid']}")
        cart_page.quick_add_item(catalog_number='', quantity='1')
        error_msg = '没有已提供的产品信息'
        assert error_msg in cart_page.find_element(*CartPageLocators.fill_out_error_msg).text

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Checkout order test')
    @allure.description('This is test of checkout order')
    def test_checkout_order(self, config, product):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        main_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('boxing', is_valid=True)
        main_page.go_to_cart_page()
        cart_page = CartPage(self.driver, config)
        cart_page.add_forgot_item_to_cart(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.go_to_order_details_page()
        cart_page.fill_order_entry(ship_to='test', bill_to='test', order_number='NA')
        cart_page.go_to_review_submit_page()
        cart_page.submit_order(is_submit=False)
        assert product['name'] in cart_page.find_element(*CartPageLocators.added_item_name_field).text
        cart_page.empty_cart()
