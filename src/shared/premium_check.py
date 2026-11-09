from typing import Optional


async def check_premium(db, user_id: str) -> bool:
    """Check if a user has premium access."""
    try:
        user = await db.users.find_one({"user_id": user_id})
        return bool(user and user.get("is_premium", False))
    except Exception:
        return False


async def has_quiz_access(db, user_id: str, quiz_id: str) -> bool:
    """Check if user has access to a quiz."""
    try:
        from database.quizzes import QuizzesRepository
        quiz_repo = QuizzesRepository(db)
        quiz = await quiz_repo.get_quiz(quiz_id)
        if not quiz:
            return False
        if not quiz.get("is_paid", False):
            return True
        is_premium = await check_premium(db, user_id)
        return is_premium or user_id == quiz.get("creator_id")
    except Exception:
        return False