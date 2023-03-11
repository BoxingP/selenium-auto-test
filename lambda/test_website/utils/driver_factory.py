from selenium import webdriver


class DriverFactory(object):

    @staticmethod
    def get_driver(browser, headless_mode=False):
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--window-size=1920,1200')
            if headless_mode is True:
                options.add_argument('--headless')
                options.add_argument("--disable-infobars")
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')
                options.add_argument('--hide-scrollbars')
                options.add_argument('--single-process')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--disable-dev-shm-usage')
                options.binary_location = '/opt/headless-chromium'
            driver = webdriver.Chrome('/opt/chromedriver', options=options)

            return driver
        raise Exception('Provide valid driver name')
