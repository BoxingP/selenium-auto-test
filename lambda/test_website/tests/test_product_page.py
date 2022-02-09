import allure
import pytest

from pages.product_page import ProductPage
from utils.locators import CartPageLocators, ProductPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestProductPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added(self, config, product):
        product_page = ProductPage(self.driver, config)
        product_page.add_product(catalog_number=product['sku'], quantity=product['quantity'])
        product_page.wait_text_to_be_display(product['name'], *ProductPageLocators.added_product_info)
        product_page.click(*ProductPageLocators.view_cart_button)
        product_page.wait_element_to_be_clickable(*CartPageLocators.empty_cart_button)
        assert product['name'] in product_page.find_element(*CartPageLocators.cart_item_name).text
