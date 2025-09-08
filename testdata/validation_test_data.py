"""
Pydantic models for structured validation test data.

This module provides comprehensive test data models for course creation form validation,
including edge cases, security testing, and business logic validation.

Key classes:
    - ValidationScenario: Enum defining all validation test scenarios
    - ValidationTestData: Base model for validation scenarios
    - EdgeCaseTestData: Model for edge case testing

Usage:
    from testdata.validation_test_data import VALIDATION_TEST_DATA, ValidationTestData
    
    @pytest.mark.parametrize("test_data", VALIDATION_TEST_DATA)
    def test_validation(self, test_data: ValidationTestData):
        # Test with structured validation data
        pass
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ValidationScenario(str, Enum):
    EMPTY_TITLE = "empty_title"
    SHORT_TITLE = "short_title"
    LONG_TITLE = "long_title"
    EMPTY_ESTIMATED_TIME = "empty_estimated_time"
    INVALID_TIME_FORMAT = "invalid_time_format"
    EMPTY_DESCRIPTION = "empty_description"
    NEGATIVE_MAX_SCORE = "negative_max_score"
    NEGATIVE_MIN_SCORE = "negative_min_score"
    MIN_GREATER_THAN_MAX = "min_greater_than_max"
    EMPTY_MAX_SCORE = "empty_max_score"
    EMPTY_MIN_SCORE = "empty_min_score"
    INVALID_CHARACTERS = "invalid_characters"
    XSS_IN_TITLE = "xss_in_title"
    SQL_INJECTION = "sql_injection"
    VALID_DATA = "valid_data"


class ValidationTestData(BaseModel):
    scenario: ValidationScenario
    title: Optional[str] = None
    estimated_time: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[str] = None
    min_score: Optional[str] = None
    expected_button_disabled: bool = True
    error_description: Optional[str] = None


VALIDATION_TEST_DATA = [
    ValidationTestData(
        scenario=ValidationScenario.EMPTY_TITLE,
        title="",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Title is required",
    ),
    ValidationTestData(
        scenario=ValidationScenario.SHORT_TITLE,
        title="ab",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Title must be at least 3 characters",
    ),
    ValidationTestData(
        scenario=ValidationScenario.LONG_TITLE,
        title="a" * 101,
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Title must be less than 100 characters",
    ),
    ValidationTestData(
        scenario=ValidationScenario.EMPTY_ESTIMATED_TIME,
        title="Test Course",
        estimated_time="",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Estimated time is required",
    ),
    ValidationTestData(
        scenario=ValidationScenario.INVALID_TIME_FORMAT,
        title="Test Course",
        estimated_time="invalid format",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Invalid time format",
    ),
    ValidationTestData(
        scenario=ValidationScenario.EMPTY_DESCRIPTION,
        title="Test Course",
        estimated_time="2 weeks",
        description="",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Description is required",
    ),
    ValidationTestData(
        scenario=ValidationScenario.NEGATIVE_MAX_SCORE,
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="-10",
        min_score="10",
        expected_button_disabled=True,
        error_description="Max score must be positive",
    ),
    ValidationTestData(
        scenario=ValidationScenario.NEGATIVE_MIN_SCORE,
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="-5",
        expected_button_disabled=True,
        error_description="Min score must be positive",
    ),
    ValidationTestData(
        scenario=ValidationScenario.MIN_GREATER_THAN_MAX,
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="50",
        min_score="100",
        expected_button_disabled=True,
        error_description="Min score cannot be greater than max score",
    ),
    ValidationTestData(
        scenario=ValidationScenario.EMPTY_MAX_SCORE,
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="",
        min_score="10",
        expected_button_disabled=True,
        error_description="Max score is required",
    ),
    ValidationTestData(
        scenario=ValidationScenario.EMPTY_MIN_SCORE,
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="",
        expected_button_disabled=True,
        error_description="Min score is required",
    ),
    ValidationTestData(
        scenario=ValidationScenario.INVALID_CHARACTERS,
        title="Test Course <>{}",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Invalid characters in title",
    ),
    ValidationTestData(
        scenario=ValidationScenario.XSS_IN_TITLE,
        title="<script>alert('xss')</script>",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="XSS attempt in title",
    ),
    ValidationTestData(
        scenario=ValidationScenario.SQL_INJECTION,
        title="'; DROP TABLE courses; --",
        estimated_time="2 weeks",
        description="Test description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="SQL injection attempt in title",
    ),
    ValidationTestData(
        scenario=ValidationScenario.VALID_DATA,
        title="Valid Course Title",
        estimated_time="2 weeks",
        description="Valid course description",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Button remains disabled without image upload",
    ),
]


class EdgeCaseTestData(BaseModel):
    scenario: str
    title: Optional[str] = None
    estimated_time: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[str] = None
    min_score: Optional[str] = None
    expected_button_disabled: bool = True
    error_description: Optional[str] = None


EDGE_CASE_TEST_DATA = [
    EdgeCaseTestData(
        scenario="unicode_emoji",
        title="Test Course 🚀",
        estimated_time="2 weeks",
        description="Test with emoji 🎯",
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Unicode emoji should be allowed (but button disabled without image)",
    ),
    EdgeCaseTestData(
        scenario="very_long_description",
        title="Test Course",
        estimated_time="2 weeks",
        description="x" * 1000,
        max_score="100",
        min_score="10",
        expected_button_disabled=True,
        error_description="Very long description should be allowed (but button disabled without image)",
    ),
    EdgeCaseTestData(
        scenario="boundary_max_score",
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="999999",
        min_score="1",
        expected_button_disabled=True,
        error_description="High max score should be allowed (but button disabled without image)",
    ),
    EdgeCaseTestData(
        scenario="equal_scores",
        title="Test Course",
        estimated_time="2 weeks",
        description="Test description",
        max_score="50",
        min_score="50",
        expected_button_disabled=True,
        error_description="Equal min and max scores should be allowed (but button disabled without image)",
    ),
]
