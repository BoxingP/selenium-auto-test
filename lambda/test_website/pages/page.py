import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Page(object):
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

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

    def open(self, url=''):
        self.driver.get(self.config['tested_page'] + url)

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

    def wait_element(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT FOUND WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            allure.attach(self.driver.get_screenshot_as_png(), name="%s not found" % (locator[1]),
                          attachment_type=AttachmentType.PNG)
            self.driver.quit()

    def wait_element_to_be_clickable(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT CLICKABLE WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            allure.attach(self.driver.get_screenshot_as_png(), name="%s not found" % (locator[1]),
                          attachment_type=AttachmentType.PNG)
            self.driver.quit()

    def wait_element_to_be_visible(self, *locator):
        timeout = self.config['timeout']
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT VISIBLE WITHIN %s SECONDS! --> %s' % (timeout, locator[1]))
            allure.attach(self.driver.get_screenshot_as_png(), name="%s not found" % (locator[1]),
                          attachment_type=AttachmentType.PNG)
            self.driver.quit()
