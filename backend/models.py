from typing import Optional
from beanie import Document, Indexed
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from pydantic import EmailStr


class User(BeanieBaseUser, Document):
    """User model for authentication"""
    email: Indexed(EmailStr, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool = True  # Default to verified
    
    class Settings:
        name = "users"
        email_collation = None


async def get_user_db():
    """Get user database instance"""
    yield BeanieUserDatabase(User)
