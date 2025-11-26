from fastapi import APIRouter, Depends
from models import User
from auth import current_active_user

router = APIRouter()

@router.get("/protected-route")
async def protected_route(user: User = Depends(current_active_user)):
    """Example protected route that requires authentication"""
    return {
        "message": f"Hello {user.email}! This is a protected route.",
        "user_id": str(user.id),
        "user_data": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified
        }
    }


@router.get("/user-profile")
async def get_user_profile(user: User = Depends(current_active_user)):
    """Get current user's profile"""
    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_verified": user.is_verified,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser
    }
