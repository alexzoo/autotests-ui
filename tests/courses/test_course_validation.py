"""Comprehensive validation tests for course creation form."""

import allure
import pytest
from allure_commons.types import Severity

from pages.courses.create_course_page import CreateCoursePage
from testdata.validation_test_data import EDGE_CASE_TEST_DATA, VALIDATION_TEST_DATA
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.routes import AppRoute


@pytest.mark.regression
@pytest.mark.courses
@pytest.mark.validation
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.story(AllureStory.COURSE_VALIDATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@allure.sub_suite(AllureStory.COURSE_VALIDATION)
class TestCourseValidation:
    """Comprehensive validation tests for course creation form."""

    @allure.severity(Severity.CRITICAL)
    @allure.title("Create button should be disabled initially")
    def test_create_button_disabled_initially(
        self, create_course_page: CreateCoursePage
    ):
        """Test that create button is disabled when form is empty."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        create_course_page.create_course_toolbar_view.check_visible()
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        create_course_page.create_course_form.check_visible(
            title="", estimated_time="", description="", max_score="0", min_score="0"
        )

        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)

    @allure.severity(Severity.CRITICAL)
    @allure.title("Create button disabled when all text fields filled but no image")
    def test_button_disabled_without_image(self, create_course_page: CreateCoursePage):
        """Test that create button remains disabled without image upload."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Fill all text fields
        create_course_page.create_course_form.fill(
            title="Valid Course Title",
            estimated_time="2 weeks",
            description="Valid course description",
            max_score="100",
            min_score="10",
        )

        # Button should remain disabled without image
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)

    @allure.severity(Severity.NORMAL)
    @allure.title("Button state changes with form validation")
    @pytest.mark.parametrize("test_data", VALIDATION_TEST_DATA)
    def test_form_validation_scenarios(
        self, test_data, create_course_page: CreateCoursePage
    ):
        """Test various form validation scenarios using parameterized data."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        @allure.step(f"Fill form with {test_data.scenario} scenario")
        def fill_form():
            create_course_page.create_course_form.fill(
                title=test_data.title or "",
                estimated_time=test_data.estimated_time or "",
                description=test_data.description or "",
                max_score=test_data.max_score or "0",
                min_score=test_data.min_score or "0",
            )

        @allure.step("Verify button state")
        def verify_button_state():
            create_course_page.create_course_toolbar_view.check_visible(
                is_create_course_disabled=test_data.expected_button_disabled
            )

        fill_form()
        verify_button_state()

    @allure.severity(Severity.NORMAL)
    @allure.title("Empty required fields validation")
    @pytest.mark.parametrize(
        "field_name",
        ["title", "estimated_time", "description", "max_score", "min_score"],
    )
    def test_empty_required_fields(
        self, field_name: str, create_course_page: CreateCoursePage
    ):
        """Test each required field individually when empty."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Fill all fields except the one being tested
        form_data = {
            "title": "Test Course",
            "estimated_time": "2 weeks",
            "description": "Test description",
            "max_score": "100",
            "min_score": "10",
        }

        # Set the tested field to empty
        form_data[field_name] = ""

        create_course_page.create_course_form.fill(**form_data)

        # Button should be disabled with any empty field
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

    @allure.severity(Severity.NORMAL)
    @allure.title("Score fields relationship validation")
    def test_score_relationship_validation(self, create_course_page: CreateCoursePage):
        """Test validation of min/max score relationship."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Test min > max (invalid)
        create_course_page.create_course_form.fill(
            title="Test Course",
            estimated_time="2 weeks",
            description="Test description",
            max_score="50",
            min_score="100",  # min > max
        )

        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        # Test valid relationship
        create_course_page.create_course_form.fill(
            title="Test Course",
            estimated_time="2 weeks",
            description="Test description",
            max_score="100",
            min_score="50",  # min < max
        )

        # Button should still be disabled due to missing image
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

    @allure.severity(Severity.NORMAL)
    @allure.title("Negative score values validation")
    def test_negative_score_validation(self, create_course_page: CreateCoursePage):
        """Test validation of negative score values."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Test negative max score
        create_course_page.create_course_form.fill(
            title="Test Course",
            estimated_time="2 weeks",
            description="Test description",
            max_score="-10",
            min_score="10",
        )

        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        # Test negative min score
        create_course_page.create_course_form.fill(
            title="Test Course",
            estimated_time="2 weeks",
            description="Test description",
            max_score="100",
            min_score="-5",
        )

        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

    @allure.severity(Severity.NORMAL)
    @allure.title("Time format validation")
    @pytest.mark.parametrize(
        "time_input,expected_disabled",
        [
            ("2 weeks", True),  # Valid format but button disabled without image
            ("1h 20m", True),  # Valid format
            ("invalid format", True),  # Invalid format
            ("", True),  # Empty
            ("-5 hours", True),  # Negative time
            ("0", True),  # Just zero
        ],
    )
    def test_time_format_validation(
        self,
        time_input: str,
        expected_disabled: bool,
        create_course_page: CreateCoursePage,
    ):
        """Test various time format inputs."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        create_course_page.create_course_form.fill(
            title="Test Course",
            estimated_time=time_input,
            description="Test description",
            max_score="100",
            min_score="10",
        )

        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=expected_disabled
        )

    @allure.severity(Severity.MINOR)
    @allure.title("Edge cases validation")
    @pytest.mark.parametrize("test_data", EDGE_CASE_TEST_DATA)
    def test_edge_cases(self, test_data, create_course_page: CreateCoursePage):
        """Test edge cases and boundary conditions."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        @allure.step(f"Testing edge case: {test_data.scenario}")
        def test_edge_case():
            create_course_page.create_course_form.fill(
                title=test_data.title or "",
                estimated_time=test_data.estimated_time or "",
                description=test_data.description or "",
                max_score=test_data.max_score or "0",
                min_score=test_data.min_score or "0",
            )

            create_course_page.create_course_toolbar_view.check_visible(
                is_create_course_disabled=test_data.expected_button_disabled
            )

        test_edge_case()

    @allure.severity(Severity.NORMAL)
    @allure.title("Real-time validation behavior")
    def test_realtime_validation(self, create_course_page: CreateCoursePage):
        """Test that validation happens in real-time as user types."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Initially button should be disabled
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        # Fill form step by step to observe real-time validation
        create_course_page.create_course_form.title_input.fill("Test Course")
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        create_course_page.create_course_form.estimated_time_input.fill("2 weeks")
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        create_course_page.create_course_form.description_textarea.fill(
            "Test description"
        )
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        create_course_page.create_course_form.max_score_input.fill("100")
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

        create_course_page.create_course_form.min_score_input.fill("10")
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )

    @allure.severity(Severity.MINOR)
    @allure.title("Form state persistence")
    def test_form_state_persistence(self, create_course_page: CreateCoursePage):
        """Test that form values persist during validation."""
        create_course_page.visit(AppRoute.COURSES_CREATE)

        # Fill form with data
        test_data = {
            "title": "Persistent Course",
            "estimated_time": "3 weeks",
            "description": "This is a test",
            "max_score": "80",
            "min_score": "20",
        }

        create_course_page.create_course_form.fill(**test_data)

        # Verify values are preserved
        create_course_page.create_course_form.check_visible(
            title=test_data["title"],
            estimated_time=test_data["estimated_time"],
            description=test_data["description"],
            max_score=test_data["max_score"],
            min_score=test_data["min_score"],
        )

        # Button should remain disabled without image
        create_course_page.create_course_toolbar_view.check_visible(
            is_create_course_disabled=True
        )
