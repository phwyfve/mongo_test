"""
Check what ID type is being used in the User model
"""
import asyncio
from models import User
from database import init_db
from beanie import PydanticObjectId

async def check_user_id_type():
    await init_db()
    
    # Find a user to check ID type
    user = await User.find_one({"email": "outrunner@live.fr"})
    if user:
        print(f"User found: {user.email}")
        print(f"User ID: {user.id}")
        print(f"User ID type: {type(user.id)}")
        print(f"Is PydanticObjectId: {isinstance(user.id, PydanticObjectId)}")
        print(f"ID as string: {str(user.id)}")
    else:
        print("No user found")

if __name__ == "__main__":
    asyncio.run(check_user_id_type())
