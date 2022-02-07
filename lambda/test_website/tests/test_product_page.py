import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.product_page import ProductPage
from utils.locators import CartPageLocators, ProductPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestProductPage:

    @pytest.mark.flaky(reruns=2, reruns_delay=5)
    @allure.title('Add product to cart test')
    @allure.description('This is test of add product to cart')
    def test_product_added(self, config):
        product_page = ProductPage(self.driver, config)
        product_page.add_product(catalog_number='26616', quantity='1')
        product_name = 'PageRuler™ 预染蛋白分子量标准，10 至 180 kDa'
        try:
            WebDriverWait(self.driver, timeout=30).until(
                EC.visibility_of_element_located(ProductPageLocators.added_product_msg)
            )
            product_page.click(*ProductPageLocators.view_cart_button)
        except TimeoutException:
            print('\n * PRODUCT ADDED PAGE NOT POPPED OUT!')
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="product added page not popped out", attachment_type=AttachmentType.PNG)
            product_page.open('store/cart')
        product_page.wait_element_to_be_visible(*CartPageLocators.order_summary_msg)
        assert product_name in product_page.find_element(*CartPageLocators.cart_item_name).text
