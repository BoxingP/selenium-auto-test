import allure

from pages.page import Page
from utils.locators import RegistrationPageLocators
from utils.logger import _step
from utils.random import random_sleep, random_password, random_boolean, random_run_functions, \
    random_phone_number, random_name
from utils.users import User


class RegistrationPage(Page):
    def __init__(self, driver, config):
        super(RegistrationPage, self).__init__(driver, config)
        self.locator = RegistrationPageLocators

    @_step
    @allure.step('Register with user: {user}')
    def register(self, user, is_exist):
        functions = [
            (self.input_first_name, []),
            (self.input_last_name, []),
            (self.input_email, [user]),
            (self.input_password, []),
            (self.select_job, []),
            (self.select_interest, [])
        ]
        random_run_functions(functions)
        is_received = random_boolean()
        if is_received:
            self.click(*self.locator.receive_info_button)
            random_sleep()
            self.scroll_page(direction='down')
            random_run_functions(
                [(self.input_company, []), (self.input_city, []), (self.input_phone_number, [])]
            )
            self.click(*self.locator.body)
        else:
            self.click(*self.locator.not_receive_info_button)
        random_sleep()
        self.click(*self.locator.create_account_button)
        if is_exist:
            self.wait_element_to_be_visible(*self.locator.registration_error)

    def input_first_name(self):
        self.input_text(random_name(), *self.locator.first_name_field)
        random_sleep()

    def input_last_name(self):
        self.input_text(random_name(), *self.locator.last_name_field)
        random_sleep()

    def input_email(self, user):
        user = User().get_user(user)
        self.input_text(user['email'], *self.locator.email_field)
        random_sleep()

    def input_password(self):
        self.input_text(random_password(), *self.locator.password_field)
        random_sleep()

    def select_job(self):
        self.click(*self.locator.job_dropdown),
        random_sleep()
        self.click(*self.locator.other_in_job_dropdown)
        random_sleep()
        self.click(*self.locator.job_dropdown)
        random_sleep()

    def select_interest(self):
        self.click(*self.locator.interest_dropdown)
        random_sleep()
        self.click(*self.locator.other_in_interest_dropdown)
        random_sleep()
        self.click(*self.locator.interest_dropdown)
        random_sleep()

    def input_company(self):
        self.input_text(random_name(), *self.locator.company_field)
        random_sleep()

    def input_city(self):
        self.input_text(random_name(), *self.locator.city_field)
        random_sleep()

    def input_phone_number(self):
        self.input_text(random_phone_number(), *self.locator.phone_number_field)
        random_sleep()
