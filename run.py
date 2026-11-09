#!/usr/bin/env python3
"""
Main entry point for the Telegram Quiz Platform.
Runs Creator Bot (Pyrogram), Runner Bot (python-telegram-bot), and Mini App (FastAPI) concurrently.
"""

import asyncio
import signal
import sys
from contextlib import asynccontextmanager

from src.shared.config import settings
from src.database import init_db, close_db
from src.creator_bot import CreatorBot
from src.runner_bot import RunnerBot
from src.mini_app import app as fastapi_app

import uvicorn


class QuizPlatform:
    """Main application orchestrator."""

    def __init__(self):
        self.creator_bot: CreatorBot | None = None
        self.runner_bot: RunnerBot | None = None
        self.fastapi_server: uvicorn.Server | None = None
        self._shutdown_event = asyncio.Event()

    async def start(self):
        """Start all services."""
        # Initialize database
        await init_db()

        # Initialize bots
        self.creator_bot = CreatorBot()
        self.runner_bot = RunnerBot()

        # Start Creator Bot (Pyrogram)
        await self.creator_bot.start()
        print("✅ Creator Bot started")

        # Start Runner Bot (python-telegram-bot)
        await self.runner_bot.start()
        print("✅ Runner Bot started")

        # Start FastAPI server for Mini App
        config = uvicorn.Config(
            fastapi_app,
            host=settings.webapp_host,
            port=settings.webapp_port,
            log_level=settings.log_level.lower(),
        )
        self.fastapi_server = uvicorn.Server(config)

        # Run FastAPI in background
        fastapi_task = asyncio.create_task(self.fastapi_server.serve())
        print(f"✅ Mini App (FastAPI) started on {settings.webapp_host}:{settings.webapp_port}")

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Graceful shutdown
        await self.shutdown(fastapi_task)

    async def shutdown(self, fastapi_task: asyncio.Task):
        """Graceful shutdown of all services."""
        print("\n🛑 Shutting down...")

        if self.creator_bot:
            await self.creator_bot.stop()
            print("✅ Creator Bot stopped")

        if self.runner_bot:
            await self.runner_bot.stop()
            print("✅ Runner Bot stopped")

        if self.fastapi_server:
            self.fastapi_server.should_exit = True
            await fastapi_task
            print("✅ Mini App stopped")

        await close_db()
        print("✅ Database connections closed")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n📡 Received signal {signum}")
        self._shutdown_event.set()


async def main():
    platform = QuizPlatform()

    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, platform.signal_handler, sig, None)

    try:
        await platform.start()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())