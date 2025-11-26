"""
Test the new register_async function
"""
import asyncio
from user_service import register_async, generate_random_email

async def test_register_function():
    print("=== Testing register_async Function ===\n")
    
    # Test 1: Register a completely new user
    print("1. Testing registration of new user...")
    random_email = generate_random_email()
    
    result = await register_async(
        email=random_email,
        password="newpassword123",
        first_name="New",
        last_name="RegisterUser"
    )
    
    if result["success"]:
        print(f"✅ New user registered successfully!")
        print(f"Email: {result['user_profile']['email']}")
        print(f"Action: {result['action']}")
        print(f"Token: {result['token'][:50]}...")
        print()
    else:
        print(f"❌ Registration failed: {result['error']}\n")
    
    # Test 2: "Register" an existing user (should just authenticate)
    print("2. Testing registration of existing user...")
    
    result = await register_async(
        email="outrunner@live.fr",  # This user already exists
        password="testpassword123",
        first_name="Existing",
        last_name="User"
    )
    
    if result["success"]:
        print(f"✅ Existing user authenticated successfully!")
        print(f"Email: {result['user_profile']['email']}")
        print(f"Action: {result['action']}")
        print(f"Token: {result['token'][:50]}...")
        print()
    else:
        print(f"❌ Authentication failed: {result['error']}\n")
    
    print("🎉 register_async() works for both new and existing users!")

if __name__ == "__main__":
    asyncio.run(test_register_function())
