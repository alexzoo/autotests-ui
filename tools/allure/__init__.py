"""
Allure reporting utilities.

This package provides enums and utilities for organizing test reports in Allure,
including epics, features, stories, and custom tags.

Key modules:
    - epics: High-level test categories (LMS)
    - features: Feature-level organization (Courses, Dashboard, etc.)
    - stories: Specific test scenarios (Course Validation, Course Deletion, etc.)
    - tags: Custom tags for test categorization
    - environment: Test environment configuration

Usage:
    from tools.allure.stories import AllureStory
    from tools.allure.features import AllureFeature
    
    @allure.feature(AllureFeature.COURSES)
    @allure.story(AllureStory.COURSE_VALIDATION)
    def test_course_validation():
        pass
"""