from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_mongo_test"
    secret_key: str = "your-super-secret-key-change-this-in-production"
    
    # Email settings
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    sendgrid_api_key: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
