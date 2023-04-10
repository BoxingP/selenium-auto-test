import allure
import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.locators import LoginPageLocators, CartPageLocators, HomePageLocators
from utils.logger import _step


@pytest.mark.usefixtures('setup', 'website_setup')
class TestHomePage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.dependency(name="open login page", scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Open login page test')
    @allure.description('This is test of open login page on home page')
    def test_login_page_opened(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        home_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_title = '登录您的账户'
        assert login_title in login_page.find_element(*LoginPageLocators.login_title).text


@pytest.mark.usefixtures('setup', 'website_setup')
class TestLoginPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.dependency(depends=["open login page"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Login with invalid user test')
    @allure.description('This is test of login with invalid user')
    def test_login_with_invalid_user(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        home_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('test', is_valid=False)
        error_msg = '用户名称或密码不正确'
        assert error_msg in login_page.find_element(*LoginPageLocators.login_error_message).text

    @pytest.mark.dependency(name="login", depends=["open login page"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Login with valid user test')
    @allure.description('This is test of login with valid user')
    def test_login_with_valid_user(self, config):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        home_page.go_to_login_page()
        login_page = LoginPage(self.driver, config)
        login_page.login('boxing', is_valid=True, save_cookie=True)
        login_page.redirect_to_home()
        profile_msg = '账户'
        assert profile_msg in login_page.find_element(*HomePageLocators.logged_in_menu).text
        login_page.logout()


@pytest.mark.usefixtures('setup', 'website_setup')
class TestCartPage:
    reruns = 2
    reruns_delay = 2

    @pytest.mark.dependency(depends=["login"], scope="session")
    @pytest.mark.flaky(reruns=reruns, reruns_delay=reruns_delay)
    @_step
    @allure.title('Checkout order test')
    @allure.description('This is test of checkout order')
    def test_checkout_order(self, config, product):
        home_page = HomePage(self.driver, config)
        home_page.open_page(f"cn/zh/home.html?cid={config['cid']}")
        if not home_page.load_cookie('boxing'):
            home_page.go_to_login_page()
            login_page = LoginPage(self.driver, config)
            login_page.login('boxing', is_valid=True, save_cookie=True)
        home_page.go_to_cart_page()
        cart_page = CartPage(self.driver, config)
        cart_page.add_forgot_item_to_cart(catalog_number=product['sku'], quantity=product['quantity'])
        cart_page.go_to_order_details_page()
        cart_page.fill_order_entry(ship_to='test', bill_to='test', order_number='NA')
        cart_page.go_to_review_submit_page()
        cart_page.submit_order(is_submit=False)
        assert product['name'] in cart_page.find_element(*CartPageLocators.added_item_name_field).text
        cart_page.empty_cart()
