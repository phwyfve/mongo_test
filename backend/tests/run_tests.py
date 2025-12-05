"""
Test suite runner for GridFS REST API tests
Provides easy way to run all tests with proper reporting
"""
import pytest
import sys
from pathlib import Path


def run_test_suite():
    """Run the complete test suite"""
    print("Starting GridFS REST API Test Suite")
    print("=" * 50)
    
    # Get the test directory
    test_dir = Path(__file__).parent
    
    # Pytest arguments for better output
    pytest_args = [
        str(test_dir),
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings for cleaner output
        "-ra",  # Show short test summary for all except passed
    ]
    
    # Run the tests
    exit_code = pytest.main(pytest_args)
    
    print("=" * 50)
    if exit_code == 0:
        print("All tests passed successfully!")
    else:
        print("Some tests failed. Check output above for details.")
    
    return exit_code


def run_specific_test(test_name):
    """Run a specific test by name"""
    test_dir = Path(__file__).parent
    pytest_args = [
        str(test_dir),
        "-v",
        "-k", test_name,
        "--tb=short"
    ]
    
    return pytest.main(pytest_args)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_test_suite()
    
    sys.exit(exit_code)
