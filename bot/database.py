"""
Database manager for E18 Meter Reader Bot using Tortoise ORM.
Handles async database initialization and repository access.
"""

import os
import logging
from tortoise import Tortoise

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages Tortoise ORM initialization and provides model access."""

    def __init__(self, database_url: str = None):
        """
        Initialize database manager.

        Args:
            database_url: PostgreSQL connection URL (defaults to DATABASE_URL env var)
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        # Convert psycopg2 URL format to asyncpg format if needed
        if self.database_url.startswith("postgresql://"):
            self.database_url = self.database_url.replace(
                "postgresql://", "postgres://"
            )

        logger.info("Database manager initialized")

    async def init(self) -> None:
        """
        Initialize Tortoise ORM and connect to database.
        Must be called at startup.
        """
        await Tortoise.init(
            db_url=self.database_url,
            modules={"models": ["bot.models"]},
        )
        await Tortoise.generate_schemas()
        logger.info("Database initialized and schemas generated")

    async def close(self) -> None:
        """Close database connections. Call at shutdown."""
        await Tortoise.close_connections()
        logger.info("Database connection closed")

    async def health_check(self) -> bool:
        """
        Check if database connection is healthy.

        Returns:
            True if connection is OK, False otherwise
        """
        try:
            # Simple query to test connection
            from bot.models import User

            await User.all().limit(1)
            logger.info("Database health check passed")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
