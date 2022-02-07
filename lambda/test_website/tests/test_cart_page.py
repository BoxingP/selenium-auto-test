import allure
import pytest

from pages.cart_page import CartPage
from utils.locators import CartPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add forgot item to cart test')
    @allure.description('This is test of add forgot item to cart')
    def test_forgot_item_added(self, config, product):
        cart_page = CartPage(self.driver, config)
        cart_page.open('store/cart')
        cart_page.add_forgot_item(catalog_number=product['sku'], quantity='1')
        cart_page.wait_element_to_be_visible(*CartPageLocators.add_success_msg)
        assert product['name'] in cart_page.find_element(*CartPageLocators.cart_item_name).text
