from enum import Enum
from typing import Self

from pydantic import DirectoryPath, EmailStr, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"


class TestUser(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TEST_USER")

    email: EmailStr
    username: str
    password: str


class TestData(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TEST_DATA")

    image_png_file: FilePath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    def get_base_url(self) -> str:
        return f"{self.app_url}/"

    app_url: HttpUrl
    headless: bool
    browsers: list[Browser] = [Browser.CHROMIUM]
    test_user: TestUser
    test_data: TestData
    videos_dir: DirectoryPath
    tracing_dir: DirectoryPath
    allure_results_dir: DirectoryPath
    browser_state_file: FilePath

    @classmethod
    def initialize(cls) -> Self:
        videos_dir = DirectoryPath("./videos")  # type: ignore
        tracing_dir = DirectoryPath("./tracing")  # type: ignore
        allure_results_dir = DirectoryPath("./allure-results")  # type: ignore
        browser_state_file = FilePath("browser-state.json")  # type: ignore

        videos_dir.mkdir(exist_ok=True)
        tracing_dir.mkdir(exist_ok=True)
        allure_results_dir.mkdir(exist_ok=True)
        browser_state_file.touch(exist_ok=True)

        return Settings(
            videos_dir=videos_dir,
            tracing_dir=tracing_dir,
            allure_results_dir=allure_results_dir,
            browser_state_file=browser_state_file,
        )  # type: ignore


settings = Settings.initialize()
