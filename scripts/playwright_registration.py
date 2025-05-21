from playwright.sync_api import sync_playwright

# Opening browser using Playwright
with sync_playwright() as playwright:
    # Launch Chromium browser in normal mode (not headless)
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context (a new session that is isolated from others)
    context = browser.new_context()
    # Open a new page within the context
    page = context.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    email_input = page.get_by_test_id("registration-form-email-input").locator("input")
    email_input.fill("user.name@gmail.com")

    username_input = page.get_by_test_id("registration-form-username-input").locator("input")
    username_input.fill("username")

    password_input = page.get_by_test_id("registration-form-password-input").locator("input")
    password_input.fill("password")

    registration_button = page.get_by_test_id("registration-page-registration-button")
    registration_button.click()

    # Save browser state (cookies and localStorage) to a file for future use
    context.storage_state(path="browser-state.json")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json")
    page = context.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/dashboard")

    page.wait_for_timeout(3000)
