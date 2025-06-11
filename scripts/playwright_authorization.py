from playwright.sync_api import expect, sync_playwright

from tools.routes import AppRoute

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(AppRoute.LOGIN)

    email_input = page.get_by_test_id("login-form-email-input").locator("input")
    email_input.fill("user.name@gmail.com")

    password_input = page.get_by_test_id("login-form-password-input").locator("input")
    password_input.fill("password")

    login_button = page.get_by_test_id("login-page-login-button")
    login_button.click()

    wrong_email_or_password_alert = page.get_by_test_id("login-page-wrong-email-or-password-alert")
    expect(wrong_email_or_password_alert).to_be_visible()
    expect(wrong_email_or_password_alert).to_have_text("Wrong email or password")

    page.wait_for_timeout(3000)
