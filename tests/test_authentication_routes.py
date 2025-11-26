"""
Integration tests for authentication routes
Tests the actual HTTP endpoints directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from user_service import generate_random_email

BASE_URL = "http://localhost:8000"

def test_authentication_routes():
    """Test the /api/authenticate and /api/register endpoints"""
    print("=== Authentication Routes Integration Test ===\n")
    
    # Test 1: Register endpoint with new user
    print("1. Testing POST /api/register with new user...")
    random_email = generate_random_email()
    
    register_data = {
        "email": random_email,
        "password": "testpassword123",
        "first_name": "Integration",
        "last_name": "TestUser"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=register_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Register successful!")
        print(f"Success: {result['success']}")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile']['email'] if result['user_profile'] else 'N/A'}")
        print(f"Token: {result['token'][:50] if result['token'] else 'None'}...")
        
        # Test the token works
        if result['token']:
            print("\n   Testing token with protected route...")
            headers = {"Authorization": f"Bearer {result['token']}"}
            protected_response = requests.get(f"{BASE_URL}/api/protected-route", headers=headers)
            print(f"   Protected route status: {protected_response.status_code}")
            if protected_response.status_code == 200:
                print("   ✅ Token works with protected route!")
            else:
                print("   ❌ Token failed with protected route")
        print()
    else:
        print(f"❌ Register failed: {response.text}\n")
    
    # Test 2: Register endpoint with existing user (should just authenticate)
    print("2. Testing POST /api/register with existing user...")
    
    existing_register_data = {
        "email": "outrunner@live.fr",  # This user already exists
        "password": "testpassword123",
        "first_name": "Existing",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=existing_register_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Register (existing user) successful!")
        print(f"Success: {result['success']}")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile']['email'] if result['user_profile'] else 'N/A'}")
        print(f"Token: {result['token'][:50] if result['token'] else 'None'}...")
        print()
    else:
        print(f"❌ Register (existing user) failed: {response.text}\n")
    
    # Test 3: Authenticate endpoint with existing user (create=False)
    print("3. Testing POST /api/authenticate with existing user (create=False)...")
    
    auth_data = {
        "email": "outrunner@live.fr",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User", 
        "create": False  # Don't create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Authenticate successful!")
        print(f"Success: {result['success']}")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile']['email'] if result['user_profile'] else 'N/A'}")
        print(f"Token: {result['token'][:50] if result['token'] else 'None'}...")
        print()
    else:
        print(f"❌ Authenticate failed: {response.text}\n")
    
    # Test 4: Authenticate endpoint with non-existing user (create=False)
    print("4. Testing POST /api/authenticate with non-existing user (create=False)...")
    
    nonexistent_email = generate_random_email()
    auth_data = {
        "email": nonexistent_email,
        "password": "testpassword123", 
        "first_name": "NonExistent",
        "last_name": "User",
        "create": False  # Don't create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print(f"✅ Unexpected success (should have failed)")
        else:
            print(f"✅ Expected failure!")
            print(f"Success: {result['success']}")
            print(f"Error: {result['error']}")
        print()
    else:
        print(f"❌ Request failed: {response.text}\n")
    
    # Test 5: Authenticate endpoint with non-existing user (create=True)  
    print("5. Testing POST /api/authenticate with non-existing user (create=True)...")
    
    another_email = generate_random_email()
    auth_data = {
        "email": another_email,
        "password": "testpassword123",
        "first_name": "Created",
        "last_name": "User",
        "create": True  # Create if doesn't exist
    }
    
    response = requests.post(f"{BASE_URL}/api/authenticate", json=auth_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Authenticate with create successful!")
        print(f"Success: {result['success']}")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile']['email'] if result['user_profile'] else 'N/A'}")
        print(f"Token: {result['token'][:50] if result['token'] else 'None'}...")
        print()
    else:
        print(f"❌ Authenticate with create failed: {response.text}\n")

def test_error_handling():
    """Test error cases"""
    print("=== Error Handling Tests ===\n")
    
    # Test invalid email format
    print("1. Testing invalid email format...")
    invalid_data = {
        "email": "not-an-email",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=invalid_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 422:  # Validation error
        print("✅ Correctly rejected invalid email")
    else:
        print(f"❌ Unexpected response: {response.text}")
    print()
    
    # Test missing password
    print("2. Testing missing password...")
    missing_password = {
        "email": "test@example.com",
        "first_name": "Test", 
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=missing_password)
    print(f"Status: {response.status_code}")
    if response.status_code == 422:  # Validation error
        print("✅ Correctly rejected missing password")
    else:
        print(f"❌ Unexpected response: {response.text}")
    print()

if __name__ == "__main__":
    try:
        test_authentication_routes()
        test_error_handling()
        print("🎉 All integration tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the FastAPI server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
