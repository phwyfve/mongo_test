import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "mongo_test_db")
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    
    # JWT settings
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Email settings
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    sendgrid_api_key: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
