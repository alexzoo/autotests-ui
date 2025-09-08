import allure
from playwright.sync_api import Page

from components.base_component import BaseComponent
from elements.button import Button
from elements.text import Text


class ConfirmationDialogComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        # Using generic selectors since the modal doesn't have specific test-id attributes
        self.title_text = Text(page, "modal-title", "Title")
        self.message_text = Text(page, "modal-message", "Message")
        self.confirm_button = Button(page, "modal-confirm-button", "Confirm")
        self.cancel_button = Button(page, "modal-cancel-button", "Cancel")

    @allure.step('Check confirmation dialog visible with title "{title}" and message "{message}"')
    def check_visible(self, title: str, message: str):
        # Use direct playwright selectors since the modal structure is different
        from playwright.sync_api import expect
        
        # Check dialog is visible
        dialog = self.page.locator("role=dialog")
        expect(dialog).to_be_visible()
        
        # Check title
        title_locator = dialog.locator("role=heading").first
        expect(title_locator).to_have_text(title)
        
        # Check message
        message_locator = dialog.locator("p", has_text=message)
        expect(message_locator).to_be_visible()
        
        # Check buttons
        confirm_locator = self.page.get_by_test_id("modal-confirm-button")
        cancel_locator = self.page.get_by_test_id("modal-cancel-button")
        expect(confirm_locator).to_be_visible()
        expect(cancel_locator).to_be_visible()

    @allure.step('Confirm deletion in confirmation dialog')
    def confirm_deletion(self):
        self.page.get_by_test_id("modal-confirm-button").click()

    @allure.step('Cancel deletion in confirmation dialog')
    def cancel_deletion(self):
        self.page.get_by_test_id("modal-cancel-button").click()

    @allure.step('Check confirmation dialog is not visible')
    def check_not_visible(self):
        from playwright.sync_api import expect
        dialog = self.page.locator("role=dialog")
        expect(dialog).to_have_count(0)