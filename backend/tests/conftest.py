"""
Shared pytest configuration and fixtures for API tests
"""
import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    print("\nSetting up test environment...")
    yield
    print("\nTest environment cleanup completed")


@pytest.fixture(scope="session")
def server_check():
    """Check if the API server is running before tests"""
    base_url = "http://localhost:8000"
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code != 200:
            pytest.skip(f"Server not responding at {base_url}")
    except requests.exceptions.ConnectionError:
        pytest.skip(f"Cannot connect to server at {base_url}. Please start the server with: python main.py")
    
    return base_url


@pytest.fixture(scope="session")
def test_user_credentials():
    """Test user credentials for authentication"""
    return {
        "email": "testuser@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
