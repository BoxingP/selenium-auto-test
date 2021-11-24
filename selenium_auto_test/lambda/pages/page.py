from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Page(object):
    def __init__(self, driver, base_url='https://www.thermofisher.cn/'):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 30

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def open(self, url=''):
        url = self.base_url + url
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def hover(self, *locator):
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def wait_element(self, *locator):
        try:
            WebDriverWait(self.driver, timeout=self.timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s' % (locator[1]))
            self.driver.quit()

    def wait_element_to_be_clickable(self, *locator):
        try:
            WebDriverWait(self.driver, timeout=self.timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            print('\n * ELEMENT NOT CLICKABLE WITHIN GIVEN TIME! --> %s' % (locator[1]))
            self.driver.quit()
