from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import User
from auth import current_active_user
from user_service import UserService
from typing import Dict, Any

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


# Request/Response models for authentication endpoints
class AuthenticateRequest(BaseModel):
    email: str
    password: str
    first_name: str = "User"
    last_name: str = "Name"
    create: bool = True

class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class AuthResponse(BaseModel):
    success: bool
    action: str = None
    token: str = None
    token_type: str = None
    user_profile: Dict[str, Any] = None
    error: str = None
    details: Dict[str, Any] = None


@router.post("/authenticate", response_model=AuthResponse)
async def authenticate_user(request: AuthenticateRequest):
    """
    Authenticate user by email. Creates user if doesn't exist and create=True.
    This is a direct route wrapper for the authenticate_email_async function.
    """
    print(f"🔍 /api/authenticate called with email: {request.email}, create: {request.create}")
    try:
        service = UserService()
        result = await service.authenticate_email_async(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            create=request.create
        )
        
        print(f"✅ Authentication result: success={result.get('success')}, action={result.get('action')}")
        return AuthResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post("/register", response_model=AuthResponse)
async def register_user(request: RegisterRequest):
    """
    Register a new user (or authenticate if already exists).
    This is a direct route wrapper for the register_async function.
    Always attempts to create the user, falls back to authentication if exists.
    """
    print(f"🔍 /api/register called with email: {request.email}")
    try:
        service = UserService()
        result = await service.authenticate_email_async(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            create=True  # Always try to create
        )
        
        print(f"✅ Registration result: success={result.get('success')}, action={result.get('action')}")
        return AuthResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


# File Management Routes (Protected)
@router.get("/files")
async def list_files(user: User = Depends(current_active_user)):
    """List user's files (protected route)"""
    # Hardcoded file list for now
    return {
        "files": [
            {
                "id": "file_001",
                "name": "document1.pdf",
                "size": "2.5 MB",
                "uploaded": "2024-11-25",
                "owner": user.email
            },
            {
                "id": "file_002", 
                "name": "presentation.pptx",
                "size": "5.1 MB",
                "uploaded": "2024-11-24",
                "owner": user.email
            },
            {
                "id": "file_003",
                "name": "spreadsheet.xlsx", 
                "size": "1.2 MB",
                "uploaded": "2024-11-23",
                "owner": user.email
            }
        ],
        "total": 3,
        "user": user.email
    }

@router.post("/files/upload")
async def upload_file(user: User = Depends(current_active_user)):
    """Upload a file (protected route - mock for now)"""
    return {
        "success": True,
        "message": "File uploaded successfully (mock)",
        "file_id": "file_new_001",
        "owner": user.email
    }

@router.delete("/files/{file_id}")
async def delete_file(file_id: str, user: User = Depends(current_active_user)):
    """Delete a file (protected route - mock for now)"""
    return {
        "success": True,
        "message": f"File {file_id} deleted successfully (mock)",
        "deleted_file_id": file_id,
        "owner": user.email
    }

@router.put("/files/{file_id}")
async def update_file(file_id: str, user: User = Depends(current_active_user)):
    """Update a file (protected route - mock for now)"""
    return {
        "success": True,
        "message": f"File {file_id} updated successfully (mock)", 
        "updated_file_id": file_id,
        "owner": user.email
    }
