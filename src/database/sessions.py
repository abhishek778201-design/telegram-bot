"""Session repository for quiz platform."""
from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient


class SessionsRepository:
    """Manages user sessions and quiz progress."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.sessions_collection = db.sessions

    async def create_session(self, user_id: str, quiz_id: str, session_type: str = "play") -> dict:
        """Create a new session for a user."""
        session_doc = {
            "user_id": user_id,
            "quiz_id": quiz_id,
            "session_type": session_type,  # play, review, practice
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "current_question_id": None,
            "score": 0,
            "created_at": datetime.utcnow(),
        }
        result = await self.sessions_collection.insert_one(session_doc)
        session_doc["_id"] = str(result.inserted_id)
        return session_doc

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session by ID."""
        if not ObjectId.is_valid(session_id):
            return None
        session = await self.sessions_collection.find_one({"_id": ObjectId(session_id)})
        if session:
            session["_id"] = str(session["_id"])
        return session

    async def update_session(self, session_id: str, **kwargs) -> Optional[dict]:
        """Update session state."""
        if not ObjectId.is_valid(session_id):
            return None
        update = {k: v for k, v in kwargs.items() if v is not None}
        if not update:
            return None
        result = await self.sessions_collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": update}
        )
        if result.matched_count > 0:
            return await self.get_session(session_id)
        return None

    async def get_user_sessions(self, user_id: str, limit: int = 50) -> list:
        """Get all sessions for a user."""
        query = {"user_id": user_id}
        cursor = self.sessions_collection.find(query).sort("started_at", -1).limit(limit)
        sessions = []
        async for session in cursor:
            session["_id"] = str(session["_id"])
            sessions.append(session)
        return sessions

    async def get_completed_sessions(self, user_id: str) -> list:
        """Get all completed sessions for a user."""
        query = {"user_id": user_id, "completed_at": {"$exists": True}}
        cursor = self.sessions_collection.find(query).sort("completed_at", -1)
        sessions = []
        async for session in cursor:
            session["_id"] = str(session["_id"])
            sessions.append(session)
        return sessions

    async def get_session_progress(self, session_id: str) -> dict:
        """Get progress details for a session."""
        session = await self.get_session(session_id)
        if not session:
            return None
        progress = {
            "current_question_id": session.get("current_question_id"),
            "score": session.get("score", 0),
            "total_questions": len(session.get("questions", [])),
            "completed_questions": sum(1 for q in session.get("questions", []) if q.get("completed", False)),
        }
        return progress
