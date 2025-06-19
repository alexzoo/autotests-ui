# autotests-ui

UI automation tests for web application testing using Playwright and Python.

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Configure environment variables in `.env` file:
- `APP_URL` - URL of the application under test
- `HEADLESS` - browser execution mode (true/false)
- `BROWSERS` - list of browsers for testing
- `TEST_USER.*` - test user credentials
- `TEST_DATA.*` - paths to test data files

## Running Tests

Run all tests:
```bash
pytest
```

Run regression tests:
```bash
pytest -m regression
```

Run tests by categories:
```bash
pytest -m courses
pytest -m dashboard
pytest -m authorization
pytest -m registration
```

Run tests in parallel:
```bash
pytest -m regression --numprocesses 2
```

Run tests with Allure report generation:
```bash
pytest -m regression --alluredir=allure-results
```

## Project Structure

- `tests/` - test scenarios
- `pages/` - page objects
- `components/` - UI components
- `elements/` - base elements
- `fixtures/` - pytest fixtures
- `tools/` - utilities and helpers

## Environment Configuration

The project uses environment variables defined in `.env` file:

```properties
APP_URL="https://nikita-filonov.github.io/qa-automation-engineer-ui-course"
HEADLESS=true
BROWSERS=["chromium"]

TEST_USER.EMAIL="user.name@gmail.com"
TEST_USER.USERNAME="username"
TEST_USER.PASSWORD="password"

TEST_DATA.IMAGE_PNG_FILE="./testdata/files/image.png"
```

