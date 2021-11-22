from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def lambda_handler(event, context):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-infobars")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--single-process')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/opt/headless-chromium'

    chrome = webdriver.Chrome('/opt/chromedriver', options=options)
    chrome.get('https://www.baidu.com/')
    WebDriverWait(driver=chrome, timeout=60).until(expected_conditions.title_is('百度一下，你就知道'))

    chrome.close()


if __name__ == "__main__":
    lambda_handler(None, None)
