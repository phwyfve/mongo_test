"""
Test script to demonstrate API functionality
Run this after starting the FastAPI server
"""
import requests
import json
import asyncio
from user_service import authenticate_email, generate_random_email

BASE_URL = "http://localhost:8000"

def test_protected_routes(access_token: str):
    """Test protected routes with given access token"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test protected route
    print("   Testing protected route...")
    response = requests.get(f"{BASE_URL}/api/protected-route", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   Error: {response.text}")
    
    # Test user profile
    print("   Testing user profile...")
    response = requests.get(f"{BASE_URL}/api/user-profile", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   Error: {response.text}")
    
    # Test user info endpoint
    print("   Testing /users/me endpoint...")
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   Error: {response.text}")
    print()

def test_api():
    print("=== FastAPI MongoDB Authentication Test ===\n")
    
    # Test root endpoint
    print("1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test with existing user (outrunner@live.fr)
    print("2. Testing authentication with existing user...")
    existing_email = "outrunner@live.fr"
    existing_password = "testpassword123"
    
    result = authenticate_email(existing_email, existing_password, create=False)
    
    if result["success"]:
        print(f"✅ Existing user authentication successful!")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile'].get('email', 'N/A')}")
        print(f"Token: {result['token'][:50]}...\n")
        
        # Test protected routes with existing user
        test_protected_routes(result["token"])
    else:
        print(f"❌ Existing user authentication failed: {result['error']}\n")
    
    # Test with new random user (should be created)
    print("3. Testing authentication with new random user...")
    random_email = generate_random_email()
    random_password = "randompassword123"
    
    result = authenticate_email(
        random_email, 
        random_password, 
        first_name="Random", 
        last_name="User", 
        create=True
    )
    
    if result["success"]:
        print(f"✅ New user authentication successful!")
        print(f"Action: {result['action']}")
        print(f"User: {result['user_profile'].get('email', 'N/A')}")
        print(f"Token: {result['token'][:50]}...\n")
        
        # Test protected routes with new user
        test_protected_routes(result["token"])
    else:
        print(f"❌ New user authentication failed: {result['error']}\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the FastAPI server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"Error: {e}")
