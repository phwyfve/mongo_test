from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models import User


async def init_db():
    """Initialize database connection and models"""
    # Create motor client
    client = AsyncIOMotorClient(settings.mongodb_url)
    
    # Initialize beanie with the User model
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User]
    )
