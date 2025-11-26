from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from auth import auth_backend, fastapi_users
from schemas import UserCreate, UserRead, UserUpdate
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await init_db()
    yield
    # Shutdown (if needed)


# Create FastAPI app
app = FastAPI(
    title="FastAPI MongoDB Authentication",
    description="A FastAPI application with MongoDB and FastAPI-Users authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Include authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Include registration route
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Include user management routes
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Include email verification routes
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# Include custom routes
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI with MongoDB and FastAPI-Users!",
        "docs": "/docs",
        "auth_endpoints": {
            "register": "/auth/register",
            "login": "/auth/jwt/login",
            "logout": "/auth/jwt/logout"
        },
        "user_endpoints": {
            "me": "/users/me",
            "protected_route": "/api/protected-route",
            "user_profile": "/api/user-profile"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
