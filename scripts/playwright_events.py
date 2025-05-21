from playwright.sync_api import Request, Response, sync_playwright


def log_request(request: Request):
    print(f"Request: {request.url}")


def log_response(response: Response):
    print(f"Response: {response.url}")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.on("request", log_request)  # Запрос отправлен
    page.on("response", log_response)  # Ответ получен

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")

    page.wait_for_timeout(3000)
