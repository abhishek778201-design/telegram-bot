from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import os


class Config(BaseSettings):
    """Centralized configuration from environment variables."""
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "quizplatform"

    BOT_TOKEN_EXTRACT: str = ""
    BOT_TOKEN_CREATOR: str = ""
    BOT_TOKEN_RUNNER: str = ""
    ADMIN_USERS: str = ""

    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    OPENAI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4"

    WEBAPP_HOST: str = "0.0.0.0"
    WEBAPP_PORT: int = 8000

    HMAC_SECRET: str = "default-secret-change-me"
    SESSION_SECRET: str = "session-change-me"

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600

    TELEGRAM_API_TIMEOUT: int = 30
    MAX_INLINE_QUERY_RESULTS: int = 50

    @field_validator("ADMIN_USERS", mode="before")
    @classmethod
    def ensure_admin_list(cls, v):
        if isinstance(v, str) and not v.startswith("?"):
            return v
        return v

    def get_admin_users(self) -> list:
        """Parse admin users list."""
        if not self.ADMIN_USERS:
            return []
        return [u.strip() for u in self.ADMIN_USERS.split(",") if u.strip()]

    def is_admin(self, user_id: str) -> bool:
        """Check if user is an admin."""
        admins = self.get_admin_users()
        return any(admin == user_id for admin in admins)

    @property
    def mongo_client(self):
        """Lazy MongoDB client."""
        from motor.motor_asyncio import AsyncIOMotorClient
        return AsyncIOMotorClient(self.MONGO_URI)

    @property
    def db(self):
        """Lazy database instance."""
        return self.mongo_client[self.MONGO_DB_NAME]

    def get_motorgb(self):
        """Get raw Motor client with database attached."""
        client = self.mongo_client
        self.mongo_client[self.MONGO_DB_NAME]
        return client

    @property
    def db_db(self):
        """Access the database directly."""
        return self.mongo_client[self.MONGO_DB_NAME]

def get_config() -> Config:
    """Initialize config with env vars."""
    os.environ.setdefault("OPENAI_API_KEY", "")
    return Config()