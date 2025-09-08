"""
Allure story definitions for test organization.

This module provides story-level categorization for Allure reports,
allowing for granular test organization and reporting.

Stories represent specific user scenarios or test categories within features.
"""

from enum import Enum


class AllureStory(str, Enum):
    """Allure story definitions for test organization."""
    
    # Core functionality stories
    COURSES = "Courses"
    COURSE_VALIDATION = "Course Validation"
    DASHBOARD = "Dashboard"
    AUTHORIZATION = "Authorization"
    REGISTRATION = "Registration"
    
    def __str__(self) -> str:
        """Return string representation for Allure reporting."""
        return self.value
