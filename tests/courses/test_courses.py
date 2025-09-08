import allure
import pytest
from allure_commons.types import Severity

from config import settings
from pages.courses.courses_list_page import CoursesListPage
from pages.courses.create_course_page import CreateCoursePage
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.routes import AppRoute


@pytest.mark.regression
@pytest.mark.courses
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.story(AllureStory.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
@allure.sub_suite(AllureStory.COURSES)
class TestCourses:
    @allure.severity(Severity.NORMAL)
    @allure.title("Empty courses list displaying")
    def test_empty_courses_list(self, courses_list_page: CoursesListPage):
        courses_list_page.visit(AppRoute.COURSES)
        courses_list_page.navbar.check_visible("username")
        courses_list_page.sidebar.check_visible()
        courses_list_page.toolbar_view.check_visible()
        courses_list_page.check_visible_empty_view()

    @allure.severity(Severity.CRITICAL)
    @allure.title("Create new course with all required fields")
    def test_create_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit(AppRoute.COURSES_CREATE)

        create_course_page.create_course_toolbar_view.check_visible()
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)
        create_course_page.create_course_form.check_visible(
            title="", estimated_time="", description="", max_score="0", min_score="0"
        )
        create_course_page.create_course_exercise_toolbar_view.check_visible()
        create_course_page.check_visible_exercises_empty_view()
        create_course_page.create_course_exercise_toolbar_view.click_create_exercise_button()

        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.create_course_form.fill(
            title="Playwright",
            estimated_time="2 weeks",
            description="Playwright",
            max_score="100",
            min_score="10",
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            title="Playwright", index=0, max_score="100", min_score="10", estimated_time="2 weeks"
        )

    @allure.severity(Severity.NORMAL)
    @allure.title("Edit existing course and save changes")
    def test_edit_course(
        self,
        create_course_page: CreateCoursePage,
        courses_list_page: CoursesListPage,
    ):
        create_course_page.visit(AppRoute.COURSES_CREATE)
        create_course_page.create_course_form.fill(
            title="Playwright",
            estimated_time="2 weeks",
            description="Playwright",
            max_score="100",
            min_score="10",
        )
        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.create_course_toolbar_view.click_create_course_button()
        courses_list_page.course_view.check_visible(
            title="Playwright", index=0, max_score="100", min_score="10", estimated_time="2 weeks"
        )

        courses_list_page.course_view.menu.click_edit(0)
        create_course_page.create_course_form.check_visible(
            title="Playwright",
            estimated_time="2 weeks",
            description="Playwright",
            max_score="100",
            min_score="10",
        )
        create_course_page.create_course_form.fill(
            title="New title", estimated_time="1 week", description="Cypress", max_score="50", min_score="20"
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()
        courses_list_page.course_view.check_visible(
            title="New title", index=0, max_score="50", min_score="20", estimated_time="1 week"
        )

    @allure.severity(Severity.CRITICAL)
    @allure.title("Delete existing course with confirmation")
    def test_delete_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit(AppRoute.COURSES_CREATE)
        
        create_course_page.create_course_form.fill(
            title="Course To Delete",
            estimated_time="3 weeks",
            description="Course for deletion test",
            max_score="80",
            min_score="30",
        )
        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()
        
        courses_list_page.course_view.check_visible(
            title="Course To Delete", index=0, max_score="80", min_score="30", estimated_time="3 weeks"
        )
        
        courses_list_page.delete_course_with_confirmation(index=0, confirm=True)
        
        courses_list_page.check_course_not_exists("Course To Delete")
        courses_list_page.check_visible_empty_view()

    @allure.severity(Severity.NORMAL)
    @allure.title("Cancel course deletion when confirmation dialog appears")
    def test_cancel_course_deletion(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit(AppRoute.COURSES_CREATE)
        
        create_course_page.create_course_form.fill(
            title="Course To Keep",
            estimated_time="4 weeks",
            description="Course for cancellation test",
            max_score="90",
            min_score="40",
        )
        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()
        
        courses_list_page.course_view.check_visible(
            title="Course To Keep", index=0, max_score="90", min_score="40", estimated_time="4 weeks"
        )
        
        courses_list_page.delete_course_with_confirmation(index=0, confirm=False)
        
        courses_list_page.course_view.check_visible(
            title="Course To Keep", index=0, max_score="90", min_score="40", estimated_time="4 weeks"
        )

    @allure.severity(Severity.NORMAL)
    @allure.title("Delete specific course from multiple courses list")
    def test_delete_course_from_multiple(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit(AppRoute.COURSES_CREATE)
        
        create_course_page.create_course_form.fill(
            title="First Course",
            estimated_time="1 week",
            description="First course for multiple deletion test",
            max_score="100",
            min_score="10",
        )
        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()
        
        create_course_page.visit(AppRoute.COURSES_CREATE)
        create_course_page.create_course_form.fill(
            title="Second Course To Delete",
            estimated_time="2 weeks",
            description="Second course for deletion test",
            max_score="80",
            min_score="20",
        )
        create_course_page.image_upload_widget.upload_preview_image(
            str(settings.test_data.image_png_file),
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()
        
        courses_list_page.visit(AppRoute.COURSES)
        
        courses_list_page.course_view.check_visible(
            title="First Course", index=0, max_score="100", min_score="10", estimated_time="1 week"
        )
        courses_list_page.course_view.check_visible(
            title="Second Course To Delete", index=1, max_score="80", min_score="20", estimated_time="2 weeks"
        )
        
        courses_list_page.delete_course_with_confirmation(index=1, confirm=True)
        
        courses_list_page.course_view.check_visible(
            title="First Course", index=0, max_score="100", min_score="10", estimated_time="1 week"
        )
        courses_list_page.check_course_not_exists("Second Course To Delete")

    @allure.severity(Severity.MINOR)
    @allure.title("Handle error when attempting to delete non-existent course")
    def test_delete_nonexistent_course_error(self, courses_list_page: CoursesListPage):
        courses_list_page.visit(AppRoute.COURSES)
        
        courses_list_page.check_visible_empty_view()
        
        courses_list_page.delete_course_expect_error(index=0)
        
        courses_list_page.check_visible_empty_view()
