"""
User service for authentication and user management
"""
import httpx
from typing import Optional, Dict, Any
import random
import string

BASE_URL = "http://localhost:8000"

class UserService:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    async def authenticate_email_async(self, email: str, password: str = "defaultpassword123", 
                                     first_name: str = "Test", last_name: str = "User", 
                                     create: bool = True) -> Dict[str, Any]:
        """
        Authenticate user by email. If user doesn't exist and create=True, creates the user first.
        Returns session data with token on success.
        
        Args:
            email: User email
            password: User password (default for new users)
            first_name: First name for new users
            last_name: Last name for new users  
            create: Whether to create user if doesn't exist
            
        Returns:
            Dict with authentication result containing token and user info
        """
        async with httpx.AsyncClient() as client:
            # First, try to login
            login_result = await self._try_login(client, email, password)
            
            if login_result["success"]:
                return login_result
            
            # If login failed and create=True, try to register first
            if create:
                print(f"User {email} doesn't exist or login failed. Attempting to create user...")
                register_result = await self._try_register(client, email, password, first_name, last_name)
                
                if register_result["success"]:
                    # Try login again after registration
                    login_result = await self._try_login(client, email, password)
                    if login_result["success"]:
                        return login_result
                    else:
                        return {
                            "success": False,
                            "error": "User created but login failed",
                            "details": login_result
                        }
                else:
                    return register_result
            else:
                return {
                    "success": False,
                    "error": "User authentication failed and create=False",
                    "details": login_result
                }
    
    async def _try_login(self, client: httpx.AsyncClient, email: str, password: str) -> Dict[str, Any]:
        """Try to login with email/password"""
        try:
            login_data = {
                "username": email,
                "password": password
            }
            
            response = await client.post(f"{self.base_url}/auth/jwt/login", data=login_data)
            
            if response.status_code == 200:
                # BearerTransport returns token in response body
                token_data = response.json()
                
                # Get user profile with the token
                headers = {"Authorization": f"Bearer {token_data['access_token']}"}
                profile_response = await client.get(f"{self.base_url}/users/me", headers=headers)
                
                user_profile = profile_response.json() if profile_response.status_code == 200 else {}
                
                return {
                    "success": True,
                    "action": "login",
                    "token": token_data["access_token"],
                    "token_type": token_data["token_type"],
                    "user_profile": user_profile,
                    "session_data": {
                        "access_token": token_data["access_token"],
                        "token_type": token_data["token_type"],
                        "user": user_profile
                    }
                }
            elif response.status_code == 204:
                # CookieTransport returns 204 with token in cookie
                # Try to extract token from cookies if available
                cookies = response.cookies
                if 'fastapiusersauth' in cookies:
                    # Cookie-based auth - we'd need to handle this differently
                    # For now, return success but note we need cookies for subsequent requests
                    return {
                        "success": True,
                        "action": "login",
                        "token": None,
                        "token_type": "cookie",
                        "user_profile": {},
                        "cookies": dict(cookies),
                        "session_data": {
                            "auth_type": "cookie",
                            "cookies": dict(cookies)
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": "Login returned 204 but no auth cookie found",
                        "response_text": response.text
                    }
            else:
                return {
                    "success": False,
                    "error": f"Login failed with status {response.status_code}",
                    "response_text": response.text
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Login request failed: {str(e)}"
            }
    
    async def _try_register(self, client: httpx.AsyncClient, email: str, password: str, 
                          first_name: str, last_name: str) -> Dict[str, Any]:
        """Try to register a new user"""
        try:
            user_data = {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name
            }
            
            response = await client.post(f"{self.base_url}/auth/register", json=user_data)
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "action": "register",
                    "user_data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Registration failed with status {response.status_code}",
                    "response_text": response.text
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Registration request failed: {str(e)}"
            }

def generate_random_email() -> str:
    """Generate a random test email"""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"testuser_{random_part}@example.com"

async def register_async(email: str, password: str, first_name: str, last_name: str) -> Dict[str, Any]:
    """
    Register a new user (or authenticate if already exists).
    This is a convenience function that always attempts to create the user.
    If the user already exists, it will just authenticate them instead.
    
    Args:
        email: User email
        password: User password
        first_name: User's first name
        last_name: User's last name
        
    Returns:
        Dict with authentication result containing token and user info
    """
    service = UserService()
    return await service.authenticate_email_async(
        email=email,
        password=password, 
        first_name=first_name, 
        last_name=last_name, 
        create=True
    )

# Synchronous wrappers for easier use in non-async contexts
def authenticate_email(email: str, password: str = "defaultpassword123", 
                      first_name: str = "Test", last_name: str = "User", 
                      create: bool = True) -> Dict[str, Any]:
    """Synchronous wrapper for authenticate_email_async"""
    import asyncio
    
    async def _run():
        service = UserService()
        return await service.authenticate_email_async(email, password, first_name, last_name, create)
    
    return asyncio.run(_run())

def register_email(email: str, password: str, first_name: str, last_name: str) -> Dict[str, Any]:
    """Synchronous wrapper for register_async"""
    import asyncio
    
    async def _run():
        return await register_async(email, password, first_name, last_name)
    
    return asyncio.run(_run())
