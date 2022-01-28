from selenium.webdriver.common.by import By


class HomePageLocators(object):
    logo_image = (By.ID, 'hfLifetechLogoImage')


class MainPageLocators(object):
    logo_image = (By.ID, 'hfLifetechLogoImage')
    my_account_menu = (By.ID, 'myaccount-button')
    sign_in_link = (By.ID, 'signIn')
    user_profile_menu = (By.ID, 'hfUserProfileLink')
    sign_out_link = (By.ID, 'hfB2cCmgtSignOutLink')


class LoginPageLocators(object):
    login_field = (By.ID, 'Thermofisher-two-step-login-username')
    username_field = (By.ID, 'username-field')
    next_button = (By.ID, 'next-button')
    password_field = (By.ID, 'password-field')
    sign_in_button = (By.ID, 'signin-button')
    login_error = (By.XPATH, '//div[@id="login-error-text"]//span[@class="error-label"]')
    login_error_message = (By.ID, 'login-error-text')


class StorePageLocators(object):
    forgot_item_catalog_number_field = (By.XPATH, '//input[@name="sku" and contains(@class, "tf-input")]')
    forgot_item_quantity_field = (By.XPATH, '//input[@name="qty" and contains(@class, "tf-input")]')
    add_forgot_to_cart_button = (By.XPATH, '//button[@type="button" and contains(@class, "tf-button1")]')
    add_success_msg = (By.XPATH, '//div[contains(@class, "line-item-success-msg")]//div[contains(@class, "tf-toast tf-toast-success")]')
    cart_item_name = (By.XPATH, '//div[@id="cartContent"]/form//div[@class="tf-row"]//div[contains(@class, "catalog-title")]')
    product_quantity_field = (By.XPATH, '//div[@class="pdp-table"]//table/tbody/tr[@class="pdp-table__selected-sku"]/td[5]/input')
    add_product_to_cart_button = (By.XPATH, '//div[@class="pdp-actions"]//div[@class="pdp-actions__buttons"]/span/button')
    view_cart = (By.XPATH, '//div[@id="cartletCartInfo"]//div[contains(@class, "cart-link-buttons") and not(contains(@class, "mobile"))]//a[@href="/store/cart"]')
    cart_info = (By.XPATH, '//div[@class="cartlet-content"]')
    order_summary = (By.XPATH, '//div[@id="orderSummary"]')
