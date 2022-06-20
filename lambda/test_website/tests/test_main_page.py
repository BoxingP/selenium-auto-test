import allure
import pytest

from pages.main_page import MainPage
from utils.locators import MainPageLocators, LoginPageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestMainPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Open login page test')
    @allure.description('This is test of open login page on main page')
    def test_login_page_opened(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        main_page.go_to_login_page()
        login_title = '登录您的账户'
        assert login_title in main_page.find_element(*LoginPageLocators.login_title).text

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check header banner exists test')
    @allure.description('This is test of check header banner exists on pages')
    def test_header_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert main_page.check_header_banner_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check yellow thin banner exists test')
    @allure.description('This is test of check yellow thin banner exists on pages')
    def test_yellow_thin_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert main_page.check_yellow_thin_banner_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check top banner exists test')
    @allure.description('This is test of check top banner exists on main page')
    def test_top_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        assert main_page.check_top_banner_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check landscape banner exists test')
    @allure.description('This is test of check landscape banner exists on pages')
    def test_landscape_banner_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert main_page.check_landscape_banner_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check order index exists test')
    @allure.description('This is test of check order index exists on main page')
    def test_order_index_exists(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home/order.html?cid={config['cid']}")
        assert main_page.check_order_index_exists()

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Search product test')
    @allure.description('This is test of search product on main page')
    def test_product_searched(self, config, product):
        main_page = MainPage(self.driver, config)
        main_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        main_page.search_product(product['sku'])
        assert product['name'] in main_page.find_element(*MainPageLocators.search_matched_product).text

    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Friendly url test')
    @allure.description('This is test of friendly url redirection')
    def test_friendly_url_redirection(self, config):
        main_page = MainPage(self.driver, config)
        main_page.open_page("https://www.thermofisher.com/covid19-flu", is_overwrite=True)
        link = 'covid19-influenza-rsv-infographic'
        assert link in main_page.get_url()
