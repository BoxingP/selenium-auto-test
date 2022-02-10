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


class CartPageLocators(object):
    forgot_item_catalog_number_field = (By.XPATH, '//input[@name="sku" and contains(@class, "tf-input")]')
    forgot_item_quantity_field = (By.XPATH, '//input[@name="qty" and contains(@class, "tf-input")]')
    add_forgot_to_cart_button = (By.XPATH, '//button[@type="button" and contains(@class, "tf-button1")]')
    cart_item_name = (By.XPATH, '//div[@id="cartContent"]/form//div[@class="tf-row"]//div[contains(@class, "catalog-title")]')
    order_summary_msg = (By.XPATH, '//div[@id="orderSummary"]')
    checkout_button = (By.XPATH, '//div[@id="mobileCheckoutButton"]/div/div/button')
    ship_recipient = (By.ID, 'shipAttn')
    bill_recipient = (By.ID, 'billAttn')
    purchase_order_number = (By.XPATH, '//div[@id="checkoutContent"]//div[@class="purchase-order__selection"]/input')
    continue_button = (By.XPATH, '//div[@id="orderSummary"]//button')
    product_items_info = (By.XPATH, '//div[@id="orderSummary"]//table/tbody/tr/td[1]')
    back_to_cart_button = (By.XPATH, '//div[@id="checkoutContent"]//div[contains(@class, "item-details")]/div/a')
    empty_cart_button = (By.XPATH, '//div[@id="cartContent"]/form//a[contains(@class, "line-item-empty")]')
    confirm_empty_cart_button = (By.XPATH, '//div[@id="empty-cart-modal"]//div/button[contains(@class, "primary-action")]')
    cart_emptied_msg = (By.XPATH, '//div[@id="cartContent"]//div/div/span[contains(@class, "strong-alt")]')


class ProductPageLocators(object):
    product_quantity_field = (By.XPATH, '//div[@id="root"]//table/tbody/tr[1]//input[@alt="item-quantity"]')
    save_to_list_button = (By.XPATH, '//div[@id="root"]//div[@class="pdp-actions"]/div/div/button')
    add_to_cart_button = (By.XPATH, '(//div[@id="root"]//div/span/button)[3]')
    added_product_info = (By.XPATH, '//div[@id="cartletCartInfo"]//div[@class="cartlet-cart-items"]//div[contains(@class, "added-to-cart-item-info")]//a/span')
    view_cart_button = (By.XPATH, '//div[@id="cartletCartInfo"]//div[contains(@class, "cart-link-buttons") and not(contains(@class, "mobile"))]//a[@href="/store/cart"]')
