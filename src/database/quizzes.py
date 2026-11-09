"""Quiz repository for quiz platform."""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient


class QuizzesRepository:
    """Manages quiz creation, editing, and storage."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.quizzes_collection = db.quizzes
        self.sections_collection = db.quiz_sections

    async def create_quiz(self, creator_id: str, title: str, description: str,
                          quiz_type: str = "standard", settings: dict = None) -> dict:
        """Create a new quiz."""
        quiz_doc = {
            "creator_id": creator_id,
            "title": title,
            "description": description,
            "quiz_type": quiz_type,  # standard, sectional, practice, exam
            "settings": settings or {},
            "questions": [],
            "sections": [],
            "is_published": False,
            "is_paid": False,
            "price": 0,
            "batch_ids": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await self.quizzes_collection.insert_one(quiz_doc)
        quiz_doc["_id"] = str(result.inserted_id)
        return quiz_doc

    async def get_quiz(self, quiz_id: str) -> Optional[dict]:
        """Retrieve quiz by ID."""
        if not ObjectId.is_valid(quiz_id):
            return None
        quiz = await self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        if quiz:
            quiz["_id"] = str(quiz["_id"])
        return quiz

    async def update_quiz(self, quiz_id: str, **kwargs) -> Optional[dict]:
        """Update quiz metadata."""
        if not ObjectId.is_valid(quiz_id):
            return None
        update = {k: v for k, v in kwargs.items() if v is not None}
        update["updated_at"] = datetime.utcnow()
        if not update:
            return None
        result = await self.quizzes_collection.update_one(
            {"_id": ObjectId(quiz_id)}, {"$set": update}
        )
        if result.matched_count > 0:
            return await self.get_quiz(quiz_id)
        return None

    async def delete_quiz(self, quiz_id: str) -> bool:
        """Delete a quiz."""
        if not ObjectId.is_valid(quiz_id):
            return False
        result = await self.quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
        await self.sections_collection.delete_many({"quiz_id": quiz_id})
        return result.deleted_count > 0

    async def add_question(self, quiz_id: str, question: dict) -> Optional[dict]:
        """Add a question to a quiz."""
        if not ObjectId.is_valid(quiz_id):
            return None
        question["question_id"] = str(ObjectId())
        question["created_at"] = datetime.utcnow()
        result = await self.quizzes_collection.update_one(
            {"_id": ObjectId(quiz_id)},
            {"$push": {"questions": question}, "$set": {"updated_at": datetime.utcnow()}}
        )
        if result.matched_count > 0:
            return await self.get_quiz(quiz_id)
        return None

    async def remove_question(self, quiz_id: str, question_id: str) -> Optional[dict]:
        """Remove a question from a quiz."""
        if not ObjectId.is_valid(quiz_id):
            return None
        result = await self.quizzes_collection.update_one(
            {"_id": ObjectId(quiz_id)},
            {"$pull": {"questions": {"question_id": question_id}},
             "$set": {"updated_at": datetime.utcnow()}}
        )
        if result.matched_count > 0:
            return await self.get_quiz(quiz_id)
        return None

    async def list_quizzes(self, creator_id: str = None, limit: int = 50) -> List[dict]:
        """List quizzes, optionally filtered by creator."""
        query = {}
        if creator_id:
            query["creator_id"] = creator_id
        cursor = self.quizzes_collection.find(query).sort("created_at", -1).limit(limit)
        quizzes = []
        async for quiz in cursor:
            quiz["_id"] = str(quiz["_id"])
            quizzes.append(quiz)
        return quizzes

    async def clone_quiz(self, quiz_id: str, new_creator_id: str) -> Optional[dict]:
        """Clone an existing quiz to a new creator."""
        quiz = await self.get_quiz(quiz_id)
        if not quiz:
            return None
        new_quiz = {
            "creator_id": new_creator_id,
            "title": f"{quiz['title']} (Copy)",
            "description": quiz["description"],
            "quiz_type": quiz["quiz_type"],
            "settings": quiz["settings"],
            "questions": quiz["questions"],
            "sections": quiz["sections"],
            "is_published": False,
            "is_paid": quiz["is_paid"],
            "price": quiz["price"],
            "batch_ids": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await self.quizzes_collection.insert_one(new_quiz)
        new_quiz["_id"] = str(result.inserted_id)
        return new_quiz

    async def add_section(self, quiz_id: str, section: dict) -> Optional[dict]:
        """Add a section to a sectional quiz."""
        if not ObjectId.is_valid(quiz_id):
            return None
        section["section_id"] = str(ObjectId())
        section["created_at"] = datetime.utcnow()
        result = await self.quizzes_collection.update_one(
            {"_id": ObjectId(quiz_id)},
            {"$push": {"sections": section}, "$set": {"updated_at": datetime.utcnow()}}
        )
        if result.matched_count > 0:
            return await self.get_quiz(quiz_id)
        return None

    async def publish_quiz(self, quiz_id: str) -> Optional[dict]:
        """Publish a quiz for use in runner bot."""
        return await self.update_quiz(quiz_id, is_published=True)

    async def unpublish_quiz(self, quiz_id: str) -> Optional[dict]:
        """Unpublish a quiz."""
        return await self.update_quiz(quiz_id, is_published=False)