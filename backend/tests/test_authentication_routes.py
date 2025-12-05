"""
Integration tests for authentication routes
Tests the actual HTTP endpoints directly using pytest
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import json
from user_service import generate_random_email

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def setup_tests():
    """Setup for authentication tests"""
    print("Starting authentication route tests...")
    yield
    print("Authentication route tests completed")

def test_register_new_user():
    """Test POST /api/register with new user"""
    random_email = generate_random_email()
    
    register_data = {
        "email": random_email,
        "password": "testpassword123",
        "first_name": "Integration",
        "last_name": "TestUser"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=register_data)
    
    assert response.status_code == 200, f"Register failed: {response.text}"
    
    result = response.json()
    assert result.get("success") == True, f"Registration not successful: {result}"
    assert result.get("token") is not None, "No token received"
    
    # Test the token works with protected route
    headers = {"Authorization": f"Bearer {result['token']}"}
    protected_response = requests.get(f"{BASE_URL}/api/protected-route", headers=headers)
    assert protected_response.status_code == 200, "Token failed with protected route"

def test_register_existing_user():
    """Test POST /api/register with existing user"""
    existing_register_data = {
        "email": "outrunner@live.fr",  # This user already exists
        "password": "testpassword123",
        "first_name": "Existing",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=existing_register_data)
    
    assert response.status_code == 200, f"Register existing user failed: {response.text}"
    
    result = response.json()
    assert result.get("success") == True, f"Registration not successful: {result}"
    assert result.get("action") == "login", "Expected login action for existing user"
    assert result.get("token") is not None, "No token received"
def test_authenticate_existing_user():
    """Test POST /api/authenticate with existing user (create=False)"""
    auth_data = {
        "email": "outrunner@live.fr",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User", 
        "create": False  # Don't create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    
    assert response.status_code == 200, f"Authenticate failed: {response.text}"
    
    result = response.json()
    assert result.get("success") == True, f"Authentication not successful: {result}"
    assert result.get("action") == "login", "Expected login action"
    assert result.get("token") is not None, "No token received"
def test_authenticate_nonexistent_user_no_create():
    """Test POST /api/authenticate with non-existing user (create=False)"""
    nonexistent_email = generate_random_email()
    auth_data = {
        "email": nonexistent_email,
        "password": "testpassword123", 
        "first_name": "NonExistent",
        "last_name": "User",
        "create": False  # Don't create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    
    assert response.status_code == 200, f"Request failed: {response.text}"
    
    result = response.json()
    assert result.get("success") == False, "Expected authentication to fail for non-existent user"
    assert "error" in result, "Expected error message"
def test_authenticate_nonexistent_user_with_create():
    """Test POST /api/authenticate with non-existing user (create=True)"""
    another_email = generate_random_email()
    auth_data = {
        "email": another_email,
        "password": "testpassword123",
        "first_name": "Created",
        "last_name": "User",
        "create": True  # Create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    
    assert response.status_code == 200, f"Authenticate with create failed: {response.text}"
    
    result = response.json()
    assert result.get("success") == True, f"Authentication not successful: {result}"
    assert result.get("token") is not None, "No token received"

def test_invalid_email_format():
    """Test invalid email format - API wraps validation errors in 200 response"""
    invalid_data = {
        "email": "not-an-email",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=invalid_data)
    
    # API wraps all errors in 200 responses with success=false
    assert response.status_code == 200, f"Expected 200 status, got {response.status_code}: {response.text}"
    
    result = response.json()
    assert result.get("success") == False, f"Expected success=false for invalid email, got: {result}"
    assert "error" in result, "Expected error field in response"
    
    # The error message should indicate validation failure
    error_msg = result.get("error", "").lower()
    assert "422" in error_msg or "failed" in error_msg, f"Error should indicate validation failure: {result.get('error')}"

if __name__ == "__main__":
    print("Starting authentication route tests...")
    pytest.main([__file__, "-v"])
    print("Authentication route tests completed")
