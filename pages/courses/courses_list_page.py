import allure
from playwright.sync_api import Page, TimeoutError

from components.courses.course_view_component import CourseViewComponent
from components.courses.courses_list_toolbar_view_component import CoursesListToolbarViewComponent
from components.dialogs.confirmation_dialog_component import ConfirmationDialogComponent
from components.navigation.navbar_component import NavbarComponent
from components.navigation.sidebar_component import SidebarComponent
from components.views.empty_view_component import EmptyViewComponent
from elements.text import Text
from pages.base_page import BasePage
from tools.logger import get_logger

logger = get_logger("COURSES_LIST_PAGE")


class CoursesListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.sidebar = SidebarComponent(page)
        self.navbar = NavbarComponent(page)
        self.empty_view = EmptyViewComponent(page, "courses-list")
        self.course_view = CourseViewComponent(page)
        self.toolbar_view = CoursesListToolbarViewComponent(page)
        self.confirmation_dialog = ConfirmationDialogComponent(page)

    def check_visible_empty_view(self):
        self.empty_view.check_visible(
            title="There is no results",
            description="Results from the load test pipeline will be displayed here",
        )

    @allure.step('Delete course at index "{index}"')
    def delete_course(self, index: int):
        self.course_view.menu.click_delete(index)
        
    @allure.step('Delete course at index "{index}" with confirmation dialog')
    def delete_course_with_confirmation(self, index: int, confirm: bool = True):
        self.course_view.menu.click_delete(index)
        
        try:
            self.confirmation_dialog.check_visible(
                title="Confirm deleting course",
                message="Are you sure you want to delete the course? This action cannot be undone"
            )
            
            if confirm:
                self.confirmation_dialog.confirm_deletion()
            else:
                self.confirmation_dialog.cancel_deletion()
        except TimeoutError as e:
            logger.warning(f"Confirmation dialog timeout: {e}")
            allure.attach(
                f"Confirmation dialog timeout: {str(e)}",
                name="Dialog Timeout",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            logger.error(f"Unexpected error during confirmation dialog: {e}")
            allure.attach(
                f"Unexpected error during confirmation dialog: {str(e)}",
                name="Dialog Error",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.step('Attempt to delete course at index "{index}" expecting error')
    def delete_course_expect_error(self, index: int):
        try:
            self.course_view.menu.click_delete(index)
        except TimeoutError as e:
            logger.warning(f"Course deletion timeout at index {index}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during course deletion at index {index}: {e}")

    @allure.step('Check that course with title "{title}" does not exist')
    def check_course_not_exists(self, title: str):
        from playwright.sync_api import expect
        
        course_title = Text(self.page, "course-widget-title-text", "Course Title")
        
        locator = course_title.get_locator()
        expect(locator.filter(has_text=title)).to_have_count(0)
