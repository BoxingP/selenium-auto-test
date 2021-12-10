import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Page(object):
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    @allure.step('Finding {locator} on the page')
    def find_element(self, *locator):
        return self.driver.find_element(*locator)

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
    def input_text(self, text, *locator):
        self.wait_element_to_be_clickable(*locator)
        self.find_element(*locator).send_keys(text)

    @allure.step('Clicking {locator} on the page')
    def click(self, *locator):
        self.wait_element_to_be_clickable(*locator)
        self.find_element(*locator).click()

    def wait_element(self, *locator):
        try:
            WebDriverWait(self.driver, timeout=self.config['timeout']).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s' % (locator[1]))
            self.driver.quit()

    def wait_element_to_be_clickable(self, *locator):
        try:
            WebDriverWait(self.driver, timeout=self.config['timeout']).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT CLICKABLE WITHIN GIVEN TIME! --> %s' % (locator[1]))
            self.driver.quit()
