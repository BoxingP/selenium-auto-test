import allure
import pytest

from pages.main_page import MainPage
from utils.locators import MainPageLocators


@pytest.mark.usefixtures('setup', 'website_setup')
class TestMainPage:

    @allure.title('Open login page test')
    @allure.description('This is test of open login page on main page')
    def test_login_page_opened(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open()
        main_page.go_to_login_page()
        link_clip = 'account-center/signin-identifie'
        assert link_clip in main_page.get_url()

    @allure.title('Open quick order page test')
    @allure.description('This is test of open quick order page on main page')
    def test_quick_order_page_opened(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open()
        self.driver.get(main_page.find_element(*MainPageLocators.quick_order_link).get_attribute('href'))
        title = 'Quick Order'
        assert title == main_page.get_title()

    @allure.title('Check promotion bar exists test')
    @allure.description('This is test of check promotion bar exists on main page')
    def test_promotion_bar_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open()
        assert main_page.is_element_exists(*MainPageLocators.promotion_bar) \
               and main_page.is_element_clickable(*MainPageLocators.promotion_bar)
        main_page.click(*MainPageLocators.app_tech_link)
        assert main_page.is_element_exists(*MainPageLocators.promotion_bar) \
               and main_page.is_element_clickable(*MainPageLocators.promotion_bar)

    @allure.title('Check thin banner exists test')
    @allure.description('This is test of check thin banner exists on main page')
    def test_thin_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open()
        assert main_page.is_element_exists(*MainPageLocators.thin_banner) \
               and main_page.is_element_clickable(*MainPageLocators.thin_banner)
        main_page.click(*MainPageLocators.app_tech_link)
        assert main_page.is_element_exists(*MainPageLocators.thin_banner) \
               and main_page.is_element_clickable(*MainPageLocators.thin_banner)

    @allure.title('Check landscape banner exists test')
    @allure.description('This is test of check landscape banner exists on main page')
    def test_landscape_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open('cn/zh/home/applications-techniques.html')
        main_page.scroll_page(direction='down')
        assert main_page.is_element_exists(*MainPageLocators.landscape_banner) \
               and main_page.is_element_clickable(*MainPageLocators.landscape_banner)
        main_page.scroll_page(direction='up')
        main_page.click(*MainPageLocators.logo_image)
        main_page.scroll_page(direction='down')
        assert main_page.is_element_exists(*MainPageLocators.landscape_banner) \
               and main_page.is_element_clickable(*MainPageLocators.landscape_banner)

    @allure.title('Check order index exists test')
    @allure.description('This is test of check order index exists on main page')
    def test_order_index_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open('order.html')
        assert main_page.find_element(*MainPageLocators.order_index_img).is_displayed() \
               and main_page.is_element_clickable(*MainPageLocators.order_index_img)

    @allure.title('Search product test')
    @allure.description('This is test of search product on main page')
    def test_product_searched(self, config, product):
        main_page = MainPage(self.driver, config)
        main_page.open()
        main_page.input_text(product['sku'], *MainPageLocators.search_product_field)
        main_page.click(*MainPageLocators.search_product_button)
        main_page.wait_element_to_be_visible(*MainPageLocators.search_product_result)
        assert product['name'] in main_page.find_element(*MainPageLocators.search_matched_product).text
