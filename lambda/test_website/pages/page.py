import os
import pickle
import time

import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.locators import PageLocators
from utils.logger import _step
from utils.screenshot import Screenshot


class Page(object):
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.locator = PageLocators

    @allure.step('Finding {locator} on the page')
    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    @allure.step('Checking {locator} whether exists on the page')
    def is_element_exists(self, *locator):
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    @_step
    @allure.step('Opening the page')
    def open_page(self, url='', is_overwrite=False):
        if is_overwrite:
            self.driver.get(url)
        else:
            self.driver.get(f"{self.config['base_url']}{url}")

    @allure.step('Getting title of the page')
    def get_title(self):
        return self.driver.title

    @allure.step('Getting url of the page')
    def get_url(self):
        return self.driver.current_url

    @allure.step('Moving mouse to {locator} on the page')
    def hover(self, *locator):
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    @allure.step('Inputting text to {locator} on the page')
    def input_text(self, text, *locator, is_overwrite=False):
        self.wait_element_to_be_clickable(*locator)
        if is_overwrite:
            self.find_element(*locator).send_keys(Keys.CONTROL + 'a')
            self.find_element(*locator).send_keys(Keys.DELETE)
        self.find_element(*locator).send_keys(text)

    @allure.step('Clicking {locator} on the page')
    def click(self, *locator):
        self.wait_element_to_be_clickable(*locator)
        self.find_element(*locator).click()

    @allure.step('Checking {locator} whether clickable on the page')
    def is_element_clickable(self, *locator):
        cursor = self.find_element(*locator).value_of_css_property("cursor")
        if cursor == "pointer":
            return True
        else:
            return False

    @allure.step('Scrolling page {direction}')
    def scroll_page(self, direction):
        html = self.find_element(*self.locator.html)
        if direction == 'up':
            html.send_keys(Keys.CONTROL + Keys.HOME)
        elif direction == 'down':
            html.send_keys(Keys.END)

    def wait_element(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT FOUND WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            Screenshot.take_screenshot(self.driver, self.config, f'{locator[1]} not found')

    def wait_element_to_be_clickable(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT CLICKABLE WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            Screenshot.take_screenshot(self.driver, self.config, f'{locator[1]} not found')

    def wait_element_to_be_visible(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT VISIBLE WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            Screenshot.take_screenshot(self.driver, self.config, f'{locator[1]} not found')

    def wait_text_to_be_display(self, text, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print('\n * %s NOT DISPLAY WITHIN %s SECONDS! --> %s' % (text, timeout, locator[1]))
            Screenshot.take_screenshot(self.driver, self.config, f'{text} not display')

    def wait_url_changed_to(self, url):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.url_contains(url))
        except TimeoutException:
            print('\n URL NOT CHANGED TO %s WITHIN %s SECONDS! --> CURRENT URL IS %s' % (url, timeout, self.get_url()))
            Screenshot.take_screenshot(self.driver, self.config, f'url not changed to {url}')

    def wait_frame_to_be_visible(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))
        except TimeoutException:
            print('\n * FRAME NOT VISIBLE WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            Screenshot.take_screenshot(self.driver, self.config, f'{locator[1]} not found')

    @_step
    @allure.step('Saving the cookie')
    def save_cookie(self, username: str):
        cookie_path = os.path.join(os.path.abspath(os.sep), 'tmp', f'{username}_cookie.pkl')
        with open(cookie_path, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)

    def is_cookie_expired(self, cookies):
        for cookie in cookies:
            if all(key in cookie for key in ('name', 'expiry')):
                if cookie['name'] == 'tokenExpiration':
                    if int(cookie['expiry']) <= int(time.time()):
                        return True
                    else:
                        return False
        return True

    @_step
    @allure.step('Loading the cookie')
    def load_cookie(self, username: str):
        try:
            cookie_path = os.path.join(os.path.abspath(os.sep), 'tmp', f'{username}_cookie.pkl')
            with open(cookie_path, 'rb') as file:
                cookies = pickle.load(file)
            if self.is_cookie_expired(cookies):
                return False
            else:
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                return True
        except FileNotFoundError:
            return False
