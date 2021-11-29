from selenium.webdriver.common.by import By


class MainPageLocators(object):
    LOGO = (By.ID, 'hfLifetechLogoImage')
    ACCOUNT = (By.ID, 'myaccount-button')
    SIGN_IN = (By.ID, 'signIn')


class LoginPageLocators(object):
    LOGIN_USERNAME = (By.ID, 'Thermofisher-two-step-login-username')
    EMAIL = (By.ID, 'username-field')
    NEXT = (By.ID, 'next-button')
    PASSWORD = (By.ID, 'password-field')
    SUBMIT = (By.ID, 'signin-button')
    ERROR_LABEL = (By.XPATH, '//div[@id="login-error-text"]//span[@class="error-label"]')
    ERROR_MESSAGE = (By.ID, 'login-error-text')
    CUSTOMER_NAME = (By.ID, 'hfCustomerName')
