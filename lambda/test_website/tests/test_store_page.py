import allure
import pytest

from pages.store_page import StorePage
from utils.locators import StorePageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestStorePage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add forgot item to cart test')
    @allure.description('This is test of add forgot item to cart')
    def test_forgot_item_added(self, config):
        store_page = StorePage(self.driver, config)
        store_page.open('store/cart')
        store_page.add_forgot_item(catalog_number='26616', quantity='1')
        product_name = 'Prestained Protein Ladder, 10 to 180 kDa'
        store_page.wait_element_to_be_visible(*StorePageLocators.add_success_msg)
        assert product_name in store_page.find_element(*StorePageLocators.cart_item_name).text

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added(self, config):
        store_page = StorePage(self.driver, config)
        store_page.open('store/cart')
        store_page.add_product(catalog_number='26616', quantity='1')
        product_name = 'Prestained Protein Ladder, 10 to 180 kDa'
        assert product_name in store_page.find_element(*StorePageLocators.cart_item_name).text
