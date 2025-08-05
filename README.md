# UI Course Automation Tests

This project implements automated tests for the [UI Course Test Application](https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login). The tests are written using **Python**, **Pytest**, **Allure** and **Playwright**. The test application's source code is available on [GitHub](https://github.com/Nikita-Filonov/qa-automation-engineer-ui-course).

## Project Overview

The goal of this project is to automate the testing of the UI Course application. The automated tests verify various functionalities of the application to ensure its stability and correctness. The project structure follows best practices for organizing test code with clear, maintainable scripts.

## Getting Started

### Clone the Repository

To get started, clone the project repository using Git:

```bash
git clone https://github.com/alexzoo/autotests-ui.git
cd autotests-ui
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies. Follow the instructions for your operating system:

#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Configure environment variables (see [Environment Configuration](#environment-configuration) section)

## Running Tests

### Basic Test Execution

Run all tests:
```bash
pytest
```

Run regression tests:
```bash
pytest -m regression
```

### Test Categories

Run tests by categories:
```bash
pytest -m courses
pytest -m dashboard
pytest -m authorization
pytest -m registration
```

### Parallel Execution

Run tests in parallel:
```bash
pytest -m regression --numprocesses 2
```

### Allure Report Generation

Run tests with Allure report generation:
```bash
pytest -m regression --alluredir=allure-results
```

### Viewing the Allure Report

After the tests have been executed, you can generate and view the Allure report with:

```bash
allure serve allure-results
```

This command will open the Allure report in your default web browser.

### UI Coverage Reports

Generate UI coverage report:
```bash
ui-coverage-tool save-report
```

View UI coverage report:
```bash
open coverage.html
```

## Project Structure

- `tests/` - test scenarios
- `pages/` - page objects
- `components/` - UI components
- `elements/` - base elements
- `fixtures/` - pytest fixtures
- `tools/` - utilities and helpers
- `coverage-results/` - UI coverage data files
- `tracing/` - Playwright trace files
- `videos/` - test execution recordings

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```properties
# Application Configuration
APP_URL="https://your-application-url.com"          # URL of the application under test
HEADLESS=true                                        # Browser execution mode (true/false)
BROWSERS=["chromium"]                                # List of browsers for testing

# Test User Credentials
TEST_USER.EMAIL="user.name@gmail.com"               # Test user email
TEST_USER.USERNAME="username"                       # Test user username
TEST_USER.PASSWORD="password"                       # Test user password

# Test Data
TEST_DATA.IMAGE_PNG_FILE="./testdata/files/image.png"  # Path to test image file

# UI Coverage Tool Configuration
UI_COVERAGE_APPS='[                                 # Applications configuration for coverage tracking
    {
        "key": "your-app-key",                      # Unique application identifier
        "url": "https://your-application-url.com",  # Application URL
        "name": "Your Application Name",            # Display name for reports
        "tags": ["UI", "AUTOMATION"],               # Tags for categorization
        "repository": "https://github.com/your-username/your-repository"  # Repository URL
    }
]'
UI_COVERAGE_HTML_REPORT_FILE="./coverage.html"      # Path to generated HTML coverage report
```

## UI Coverage Tool

The project integrates `ui-coverage-tool` for tracking UI element interactions and generating coverage reports:

- **Purpose**: Tracks which UI elements are being tested and how often
- **Report Generation**: Creates visual HTML reports showing element usage statistics
- **Integration**: Automatically tracks interactions with PageFactory elements
- **History**: Maintains coverage history across test runs

### Coverage Report Features:
- Visual representation of element usage
- Historical data tracking
- Detailed statistics per UI component
- Export capabilities for further analysis
