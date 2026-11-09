# MongoDB Database Repositories for Quiz Platform

from .users import UsersRepository
from .quizzes import QuizzesRepository
from .payments import PaymentsRepository
from .sessions import SessionsRepository
from .analytics import AnalyticsRepository

__all__ = [
    "UsersRepository",
    "QuizzesRepository",
    "PaymentsRepository",
    "SessionsRepository",
    "AnalyticsRepository",
]