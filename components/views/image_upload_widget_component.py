from playwright.sync_api import Page

from components.base_component import BaseComponent
from components.views.empty_view_component import EmptyViewComponent
from elements.button import Button
from elements.file_input import FileInput
from elements.icon import Icon
from elements.image import Image
from elements.text import Text


class ImageUploadWidgetComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        self.preview_empty_view = EmptyViewComponent(page)

        self.preview_image = Image(
            page,
            "{identifier}-image-upload-widget-preview-image",
            "Preview",
        )

        self.image_upload_info_icon = Icon(
            page,
            "{identifier}-image-upload-widget-info-icon",
            "Upload info",
        )
        self.image_upload_info_title = Text(
            page, "{identifier}-image-upload-widget-info-title-text", "Upload info"
        )
        self.image_upload_info_description = Text(
            page, "{identifier}-image-upload-widget-info-description-text", "Upload info"
        )

        self.upload_button = Button(
            page,
            "{identifier}-image-upload-widget-upload-button",
            "Upload",
        )
        self.remove_button = Button(
            page,
            "{identifier}-image-upload-widget-remove-button",
            "Remove",
        )
        self.upload_input = FileInput(page, "{identifier}-image-upload-widget-input", "Upload")

    def check_visible(self, identifier: str, is_image_uploaded: bool = False):
        # expect(self.image_upload_info_icon).to_be_visible()
        self.image_upload_info_icon.check_visible(identifier=identifier)

        # expect(self.image_upload_info_title).to_be_visible()
        # expect(self.image_upload_info_title).to_have_text('Tap on "Upload image" button to select file')
        self.image_upload_info_title.check_visible(identifier=identifier)
        self.image_upload_info_title.check_have_text(
            'Tap on "Upload image" button to select file', identifier=identifier
        )

        # expect(self.image_upload_info_description).to_be_visible()
        # expect(self.image_upload_info_description).to_have_text("Recommended file size 540X300")
        self.image_upload_info_description.check_visible(identifier=identifier)
        self.image_upload_info_description.check_have_text(
            "Recommended file size 540X300", identifier=identifier
        )

        # expect(self.upload_button).to_be_visible()
        self.upload_button.check_visible(identifier=identifier)

        if is_image_uploaded:
            # expect(self.remove_button).to_be_visible()
            # expect(self.preview_image).to_be_visible()
            self.remove_button.check_visible(identifier=identifier)
            self.preview_image.check_visible(identifier=identifier)

        if not is_image_uploaded:
            self.preview_empty_view.check_visible(
                title="No image selected",
                description="Preview of selected image will be displayed here",
                identifier=identifier,
            )

    def click_remove_image_button(self, identifier: str):
        self.remove_button.click(identifier=identifier)

    def upload_preview_image(self, file: str, identifier: str):
        self.upload_input.set_input_files(file, identifier=identifier)
