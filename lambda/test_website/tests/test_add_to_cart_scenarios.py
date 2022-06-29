import allure
import pytest

from pages.cart_page import CartPage
from pages.product_page import ProductPage
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


@pytest.mark.usefixtures('setup', 'website_setup')
class TestProductPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added_to_cart(self, config, product):
        catalog_number = product['sku']
        product_name = product['name']
        quantity = product['quantity']
        product_page = ProductPage(self.driver, config)
        product_page.open_page(f"order/catalog/product/{catalog_number}?cid={config['cid']}")
        product_page.add_product(catalog_number=catalog_number, product_name=product_name, quantity=quantity)
        product_page.go_to_cart_page()
        assert product_name in product_page.find_element(*CartPageLocators.cart_item_name).text
