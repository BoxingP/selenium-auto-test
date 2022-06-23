import random

from selenium.webdriver.common.by import By


class PageLocators(object):
    body = (By.XPATH, '//body')
    html = (By.TAG_NAME, 'html')


class HomePageLocators(PageLocators):
    logo_image = (By.ID, 'hfLifetechLogoImage')


class MainPageLocators(PageLocators):
    logo_image = (By.ID, 'hfLifetechLogoImage')
    my_account_menu = (By.ID, 'myaccount-button')
    sign_in_link = (By.ID, 'signIn')
    user_profile_menu = (By.ID, 'hfUserProfileLink')
    sign_out_link = (By.ID, 'hfB2cCmgtSignOutLink')
    registration_link = (By.XPATH, '//div[@id="myaccount-div"]/div[1]/p/a[2]')
    account_link = (By.XPATH, '//div[@id="myaccount-div"]/div/div[2]/div/li[2]/a')
    my_cart = (By.ID, 'viewMiniCart')
    header_banner = (By.XPATH, '//div[@id="promoBarContent"]/a')
    yellow_thin_banner = (By.XPATH, '//div[contains(@class, "thinbanner")]/a')
    top_banner = (By.ID, 'ggBox')
    landscape_banner = (By.XPATH, '//div[@id="landscapeBannerContent"]/a')
    order_index_container = (By.XPATH, '//div[@container-id="cq-colctrl-lt1" and @comp-id="B1"]')
    order_index_img = (By.XPATH, '(//a/div/picture/img)[1]')
    search_product_field = (By.ID, 'suggest1')
    search_product_button = (By.ID, 'searchButton')
    search_product_result = (By.XPATH, '//div[@id="mainContent"]//div[@class="utility-bar-content"]/span')
    search_matched_product = (By.XPATH, '//div[@id="mainContent"]//h2/a[@data-res_pos="1"]')
    online_chat_frame = (By.ID, 'ymIframe')
    online_chat_button = (By.ID, 'ymDivCircle')
    online_chat_title = (By.XPATH, '//div[@id="chatDetails"]/div[1]')
    online_chat_message = (By.XPATH, '//div[@id="chatBoxMain"]/div[1]/div')


class LoginPageLocators(PageLocators):
    login_title = (By.XPATH, '//body[@id="login-app-body"]/div/div/div/div/p')
    username_field = (By.ID, 'username-field')
    next_button = (By.ID, 'next-button')
    password_field = (By.ID, 'password-field')
    sign_in_button = (By.ID, 'signin-button')
    login_error = (By.XPATH, '//div[@id="login-error-text"]//span[@class="error-label"]')
    login_error_message = (By.ID, 'login-error-text')


class RegistrationPageLocators(PageLocators):
    last_name_field = (By.XPATH, '//div[@id="fields"]/app-form-input[1]/div/input')
    first_name_field = (By.XPATH, '//div[@id="fields"]/app-form-input[2]/div/input')
    email_field = (By.XPATH, '//div[@id="email"]/input')
    password_field = (By.ID, 'reg-form-password')
    job_dropdown = (By.XPATH, '//div[@id="fields"]/div[3]/app-custom-dropdown/div/button')
    jobs_in_job_dropdown = (By.XPATH, f'//div[@id="fields"]/div[3]//li[@id="{random.randrange(10)}"]/label')
    interest_dropdown = (By.XPATH, '//div[@id="fields"]/div[4]/app-custom-dropdown/div/button')
    interests_in_interest_dropdown = (By.XPATH, f'//div[@id="fields"]/div[4]//*[@id="{random.randrange(11)}"]/label')
    receive_info_button = (By.XPATH, '//div[@id="consent"]/app-consent/div/app-radio-button/div[1]/label')
    not_receive_info_button = (By.XPATH, '//div[@id="consent"]/app-consent/div/app-radio-button/div[2]/label')
    company_field = (By.XPATH, '//div[@id="extra-fields"]/div[1]/input')
    city_field = (By.XPATH, '//div[@id="extra-fields"]/div[2]/input')
    phone_number_field = (By.XPATH, '//div[@id="extra-fields"]/div[4]/input')
    create_account_button = (By.ID, 'create-account-button')
    registration_error = (By.ID, 'toast-container')
    registration_error_message = (By.XPATH, '//div[@id="toast-container"]/div/div[2]/span/div[1]/div[2]/span')


class CartPageLocators(PageLocators):
    forgot_item_catalog_number_field = (By.XPATH, '//input[@name="sku" and contains(@class, "tf-input")]')
    forgot_item_quantity_field = (By.XPATH, '//input[@name="qty" and contains(@class, "tf-input")]')
    add_forgot_to_cart_button = (By.XPATH, '//div[@id="cartContent"]//button[not(@id="clearItems")]')
    cart_item_name = (By.XPATH, '//div[@id="cartContent"]/form//div[@class="tf-row"]//div[contains(@class, "catalog-title")]')
    checkout_button = (By.XPATH, '//div[@id="mobileCheckoutButton"]/div/div/button')
    ship_recipient = (By.XPATH, '//div[@class="shipping-billing-cards"]/div[contains(@class, "shipping-card")]//input[@data-testid="attentionTo"]')
    bill_recipient = (By.XPATH, '//div[@class="shipping-billing-cards"]/div[contains(@class, "billing-card")]//input[@data-testid="attentionTo"]')
    purchase_order_number = (By.XPATH, '//div[contains(@class, "payment-methods")]/div/div/div/div/input')
    continue_button = (By.XPATH, '//div[@class="sticky-order-summary"]/div/div/button')
    terms_conditions_accept_button = (By.XPATH, '//div[@class="ck-terms-conditions"]/label')
    terms_conditions_msg = (By.XPATH, '//div[@class="ck-terms-conditions"]/label/div')
    submit_order_button = (By.XPATH, '//div[@class="sticky-order-summary"]/div/div/button')
    back_to_cart_button = (By.XPATH, '//div[@class="review-and-submit"]/div[3]/div/div/button')
    added_item_name_field = (By.XPATH, '(//div[@id="cartContent"]//div[@class="tf-row"]/div/div/a/div)[1]')
    empty_cart_button = (By.XPATH, '//div[@id="cartContent"]/form//a[contains(@class, "line-item-empty")]')
    confirm_empty_cart_button = (By.XPATH, '//div[@id="empty-cart-modal"]//div/button[contains(@class, "primary-action")]')
    cart_emptied_msg = (By.XPATH, '//div[@id="cartContent"]//div/div/span[contains(@class, "strong-alt")]')
    quick_add_catalog_number_field = (By.XPATH, '//div[contains(@class, "quick-order")]//table/tbody[1]/tr/td[1]/input')
    quick_add_quantity_field = (By.XPATH, '//div[contains(@class, "quick-order")]//table/tbody[1]/tr/td[2]/input')
    quick_add_product_to_cart_button = (By.XPATH, '//div[contains(@class, "quick-order-app")]//div[contains(@class, "quick-order")]//form/div/div/button[2]')
    fill_out_error_msg = (By.XPATH, '//div[@class="container-wrap"]//form/div/div[3]/div')


class ProductPageLocators(PageLocators):
    product_quantity_field = (By.XPATH, '//div[@id="root"]//table/tbody/tr[1]//input[@alt="item-quantity"]')
    save_to_list_button = (By.XPATH, '//div[@id="root"]//div[@class="pdp-actions"]/div/div/button')
    add_to_cart_button = (By.XPATH, '//div[@id="root"]//div[@class="pdp-actions"]/div/div/span/button')
    added_product_info = (By.XPATH, '//div[@id="cartletCartInfo"]//div[@class="cartlet-cart-items"]//div[contains(@class, "added-to-cart-item-info")]//a/span')
    view_cart_button = (By.XPATH, '//div[@id="cartletCartInfo"]//div[contains(@class, "cart-link-buttons") and not(contains(@class, "mobile"))]//a[@href="/store/cart"]')


class AccountPageLocators(PageLocators):
    order_history_link = (By.XPATH, '//div[@id="root"]//div[@class="nav-container"]/div/div[3]/div[2]/div/div[1]/a')
    order_history_record = (By.XPATH, '//div[@id="root"]/div/div[2]/div/table/tbody/tr')
