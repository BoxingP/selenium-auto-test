import unittest

from selenium import webdriver


class Test(unittest.TestCase):

    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--single-process')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.binary_location = '/opt/headless-chromium'

        self.driver = webdriver.Chrome('/opt/chromedriver', options=options)

    def tearDown(self) -> None:
        self.driver.close()
