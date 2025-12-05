"""
Pytest tests for Authentication Service functionality
Tests the UserService class and protected routes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import json
from user_service import authenticate_email, generate_random_email

BASE_URL = "http://localhost:8000"

def verify_protected_routes(access_token: str):
    """Verify protected routes work with given access token"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test protected route
    response = requests.get(f"{BASE_URL}/api/protected-route", headers=headers)
    assert response.status_code == 200, f"Protected route failed: {response.text}"
    
    result = response.json()
    assert "message" in result, "Protected route should return message"
    assert "user_id" in result, "Protected route should return user_id"
    assert "user_data" in result, "Protected route should return user_data"
    
    # Test user profile
    response = requests.get(f"{BASE_URL}/api/user-profile", headers=headers)
    assert response.status_code == 200, f"User profile failed: {response.text}"
    
    profile = response.json()
    assert "email" in profile, "Profile should contain email"
    assert "first_name" in profile, "Profile should contain first_name"
    assert "last_name" in profile, "Profile should contain last_name"
    
    # Test FastAPI-Users /users/me endpoint
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    assert response.status_code == 200, f"Users/me endpoint failed: {response.text}"
    
    user_data = response.json()
    assert "email" in user_data, "User data should contain email"
    assert "id" in user_data, "User data should contain id"
    
    return profile

@pytest.fixture(scope="session", autouse=True)
def setup_service_tests():
    """Setup for authentication service tests"""
    print("Starting authentication service tests...")
    yield
    print("Authentication service tests completed")

def test_root_endpoint():
    """Test root endpoint is accessible"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Root endpoint failed: {response.text}"
    
    result = response.json()
    assert "message" in result, "Root endpoint should return a message"

def test_existing_user_authentication():
    """Test authentication with existing user (no creation)"""
    existing_email = "outrunner@live.fr"
    existing_password = "testpassword123"
    
    result = authenticate_email(existing_email, existing_password, create=False)
    
    assert result["success"] == True, f"Existing user authentication failed: {result.get('error')}"
    assert result["action"] == "login", f"Expected login action, got: {result.get('action')}"
    assert result["token"] is not None, "Authentication should return a token"
    assert result["user_profile"] is not None, "Authentication should return user profile"
    assert result["user_profile"]["email"] == existing_email, "Profile email should match"
    
    # Verify protected routes work
    profile = verify_protected_routes(result["token"])
    assert profile["email"] == existing_email, "Profile email should match authenticated user"

def test_new_user_creation_and_authentication():
    """Test creating new user and authenticating"""
    random_email = generate_random_email()
    random_password = "randompassword123"
    
    result = authenticate_email(
        random_email, 
        random_password, 
        first_name="Random", 
        last_name="User", 
        create=True
    )
    
    assert result["success"] == True, f"New user creation failed: {result.get('error')}"
    assert result["token"] is not None, "New user should get authentication token"
    assert result["user_profile"] is not None, "New user should have profile"
    assert result["user_profile"]["email"] == random_email, "Profile email should match"
    assert result["user_profile"]["first_name"] == "Random", "Profile first_name should match"
    assert result["user_profile"]["last_name"] == "User", "Profile last_name should match"
    
    # Verify protected routes work for new user
    profile = verify_protected_routes(result["token"])
    assert profile["email"] == random_email, "Profile email should match new user"

def test_nonexistent_user_no_creation():
    """Test authentication fails for non-existent user when create=False"""
    nonexistent_email = generate_random_email()
    nonexistent_password = "somepassword123"
    
    result = authenticate_email(nonexistent_email, nonexistent_password, create=False)
    
    assert result["success"] == False, "Authentication should fail for non-existent user with create=False"
    assert "error" in result, "Failed authentication should include error message"
    assert result.get("token") is None, "Failed authentication should not return token"

if __name__ == "__main__":
    print("Starting authentication service tests...")
    pytest.main([__file__, "-v"])
    print("Authentication service tests completed")
