import allure

from pages.page import Page
from utils.locators import AccountPageLocators
from utils.logger import _step
from utils.users import User


class AccountPage(Page):
    def __init__(self, driver, config):
        super(AccountPage, self).__init__(driver, config)
        self.locator = AccountPageLocators

    @_step
    @allure.step('Open order history page')
    def go_to_order_history_page(self):
        self.click(*self.locator.order_history_link)
        self.wait_url_changed_to('history')

    @_step
    @allure.step('Check order history exists')
    def check_order_history_exists(self):
        if self.is_element_exists(*self.locator.order_history_record):
            return True
        else:
            return False

    @_step
    @allure.step('Open personal profile page')
    def go_to_personal_profile_page(self):
        self.click(*self.locator.personal_profile_link)
        self.wait_url_changed_to('profile')

    @_step
    @allure.step('Check billing address exists')
    def check_billing_address_exists(self, user):
        user = User().get_user(user)
        if user['billing_account'] == self.find_element(*self.locator.billing_account_field).text:
            return True
        else:
            return False

    @_step
    @allure.step('Check shipping address exists')
    def check_shipping_address_exists(self, user):
        user = User().get_user(user)
        if user['shipping_account'] == self.find_element(*self.locator.shipping_account_field).text:
            return True
        else:
            return False
