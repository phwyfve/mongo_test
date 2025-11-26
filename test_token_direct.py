"""
Direct token validation test
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_token_validation():
    print("=== Direct Token Validation Test ===\n")
    
    # First, get a token by logging in
    print("1. Getting token via login...")
    login_data = {
        "username": "outrunner@live.fr",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
    print(f"Login Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"Token received: {access_token[:50]}...")
        print(f"Token type: {token_data['token_type']}")
        
        # Test the token immediately
        print("\n2. Testing token immediately...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Test /users/me first (built-in FastAPI-Users endpoint)
        print("Testing /users/me...")
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
            print(f"Response headers: {dict(response.headers)}")
        
        # Test custom protected route
        print("\nTesting /api/protected-route...")
        response = requests.get(f"{BASE_URL}/api/protected-route", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
            print(f"Response headers: {dict(response.headers)}")
            
    else:
        print(f"Login failed: {response.text}")
        print(f"Response headers: {dict(response.headers)}")

if __name__ == "__main__":
    test_token_validation()
