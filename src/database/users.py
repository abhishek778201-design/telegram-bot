"""User repository for quiz platform."""
from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient


class UsersRepository:
    """Manages user accounts and profiles."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.users_collection = db.users

    async def create_user(self, username: str, email: str, password_hash: str) -> dict:
        """Create a new user account."""
        user_id = await self.users_collection.insert_one({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
            "is_premium": False,
            "is_owner": False,
        }).insert_id
        return {"user_id": str(user_id), "username": username, "email": email}

    async def get_user(self, user_id: str) -> Optional[dict]:
        """Retrieve user by ID."""
        return await self.users_collection.find_one({"user_id": user_id})

    async def update_user(self, user_id: str, **kwargs) -> Optional[dict]:
        """Update user profile."""
        update = {k: v for k, v in kwargs.items() if v is not None}
        if not update:
            return None
        result = await self.users_collection.update_one(
            {"user_id": user_id}, {"$set": update}
        )
        if result.matched_count > 0:
            return await self.users_collection.find_one({"user_id": user_id})
        return None

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user account."""
        result = await self.users_collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    async def list_users(self, limit: int = 100) -> list:
        """List all users (paginated)."""
        cursor = self.users_collection.find().limit(limit)
        return list(cursor)

    async def get_premium_users(self) -> list:
        """Get all premium users."""
        return list(self.users_collection.find({"is_premium": True}).limit(100))

    async def get_owner(self) -> Optional[dict]:
        """Get the platform owner."""
        return await self.users_collection.find_one({"is_owner": True})
