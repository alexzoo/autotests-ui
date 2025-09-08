"""
Test data management package.

This package provides structured test data management using Pydantic models
for consistent and maintainable test data across the test suite.

Key modules:
    - validation_test_data: Pydantic models for validation testing
    - files: Static test files and resources

Usage:
    from testdata.validation_test_data import VALIDATION_TEST_DATA, ValidationTestData
    
    @pytest.mark.parametrize("test_data", VALIDATION_TEST_DATA)
    def test_validation(self, test_data: ValidationTestData):
        # Use structured test data
        pass
"""