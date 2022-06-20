import allure

from pages.page import Page
from utils.locators import AccountPageLocators
from utils.logger import _step


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
