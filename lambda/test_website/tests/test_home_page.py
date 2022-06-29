import allure
import pytest

from pages.home_page import HomePage
from utils.locators import HomePageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestHomePage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.dependency(name="home", scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Open home page test')
    @allure.description('This is test of open home page')
    def test_page_loaded(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        assert home_page.check_page_loaded()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check header banner exists test')
    @allure.description('This is test of check header banner exists on pages')
    def test_header_banner_exists(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert home_page.check_header_banner_exists()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check yellow thin banner exists test')
    @allure.description('This is test of check yellow thin banner exists on pages')
    def test_yellow_thin_banner_exists(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert home_page.check_yellow_thin_banner_exists()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check top banner exists test')
    @allure.description('This is test of check top banner exists on home page')
    def test_top_banner_exists(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        assert home_page.check_top_banner_exists()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check landscape banner exists test')
    @allure.description('This is test of check landscape banner exists on pages')
    def test_landscape_banner_exists(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home/applications-techniques.html?cid={config['cid']}")
        assert home_page.check_landscape_banner_exists()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Check order index exists test')
    @allure.description('This is test of check order index exists on page')
    def test_order_index_exists(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home/order.html?cid={config['cid']}")
        assert home_page.check_order_index_exists()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Search product test')
    @allure.description('This is test of search product on home page')
    def test_product_searched(self, config, product):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        home_page.search_product(product['sku'])
        assert product['name'] in home_page.find_element(*HomePageLocators.search_matched_product).text

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Friendly url test')
    @allure.description('This is test of friendly url redirection')
    def test_friendly_url_redirection(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page("https://www.thermofisher.com/covid19-flu", is_overwrite=True)
        link = 'covid19-influenza-rsv-infographic'
        assert link in home_page.get_url()

    @pytest.mark.dependency(depends=["home"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Online chat test')
    @allure.description('This is test of online chat opening')
    def test_online_chat_opening(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        home_page.open_online_chat()
        title = '为您服务'
        assert title in home_page.find_element(*HomePageLocators.online_chat_message).text
