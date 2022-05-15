import allure
import pytest

from pages.product_page import ProductPage
from utils.locators import CartPageLocators, ProductPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestProductPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @_step
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added_to_cart(self, config, product):
        catalog_number = product['sku']
        product_name = product['name']
        quantity = product['quantity']
        product_page = ProductPage(self.driver, config)
        product_page.open_page(f"order/catalog/product/{catalog_number}?cid={config['cid']}")
        product_page.wait_element_to_be_clickable(*ProductPageLocators.save_to_list_button)
        product_page.add_product(catalog_number=catalog_number, product_name=product_name, quantity=quantity)
        product_page.go_to_cart_page()
        assert product_name in product_page.find_element(*CartPageLocators.cart_item_name).text
