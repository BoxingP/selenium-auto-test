import allure
import pytest

from pages.cart_page import CartPage
from utils.locators import CartPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add forgot item to cart test')
    @allure.description('This is test of add forgot item to cart')
    def test_forgot_item_added(self, config):
        cart_page = CartPage(self.driver, config)
        cart_page.open('store/cart')
        cart_page.add_forgot_item(catalog_number='26616', quantity='1')
        product_name = 'Prestained Protein Ladder, 10 to 180 kDa'
        cart_page.wait_element_to_be_visible(*CartPageLocators.add_success_msg)
        assert product_name in cart_page.find_element(*CartPageLocators.cart_item_name).text
