import allure
import pytest

from pages.product_page import ProductPage
from utils.locators import CartPageLocators, ProductPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestProductPage:

    @_step
    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added_to_cart(self, config, product):
        catalog_number = product['sku']
        quantity = product['quantity']
        product_page = ProductPage(self.driver, config)
        product_page.open_page(f"order/catalog/product/{catalog_number}?cid={config['cid']}")
        product_page.wait_element_to_be_clickable(*ProductPageLocators.save_to_list_button)
        product_page.add_product(catalog_number=catalog_number, quantity=quantity)
        product_page.wait_text_to_be_display(product['name'], *ProductPageLocators.added_product_info)
        product_page.click(*ProductPageLocators.view_cart_button)
        product_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        assert product['name'] in product_page.find_element(*CartPageLocators.cart_item_name).text
