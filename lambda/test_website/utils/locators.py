from selenium.webdriver.common.by import By


class PageLocators(object):
    html = (By.TAG_NAME, 'html')


class HomePageLocators(PageLocators):
    logo_image = (By.ID, 'hfLifetechLogoImage')


class MainPageLocators(PageLocators):
    logo_image = (By.ID, 'hfLifetechLogoImage')
    my_account_menu = (By.ID, 'myaccount-button')
    sign_in_link = (By.ID, 'signIn')
    user_profile_menu = (By.ID, 'hfUserProfileLink')
    sign_out_link = (By.ID, 'hfB2cCmgtSignOutLink')
    my_cart = (By.ID, 'viewMiniCart')
    header_banner = (By.XPATH, '//div[@id="promoBarContent"]/a')
    app_tech_link = (By.XPATH, '//ul[@id="meganav-content"]/li[2]/a')
    yellow_thin_banner = (By.XPATH, '//div[contains(@class, "thinbanner")]/a')
    top_banner = (By.ID, 'ggBox')
    landscape_banner = (By.XPATH, '//div[@id="landscapeBannerContent"]/a')
    order_index_img = (By.XPATH, '//a/div/picture/img')
    search_product_field = (By.ID, 'suggest1')
    search_product_button = (By.ID, 'searchButton')
    search_product_result = (By.XPATH, '//div[@id="mainContent"]//div[@class="utility-bar-content"]/span')
    search_matched_product = (By.XPATH, '//div[@id="mainContent"]//h2/a[@data-res_pos="1"]')


class LoginPageLocators(PageLocators):
    login_title = (By.XPATH, '//body[@id="login-app-body"]/div/div/div/div/p')
    username_field = (By.ID, 'username-field')
    next_button = (By.ID, 'next-button')
    password_field = (By.ID, 'password-field')
    sign_in_button = (By.ID, 'signin-button')
    login_error = (By.XPATH, '//div[@id="login-error-text"]//span[@class="error-label"]')
    login_error_message = (By.ID, 'login-error-text')


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
