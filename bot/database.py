"""
Database manager for E18 Meter Reader Bot.
Handles database connection and repository initialization.
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import logging

from bot.repositories import (
    UsersRepository,
    ApartmentsRepository,
    MetersRepository,
    UserRolesRepository,
    ReadingsRepository,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connection and provides repository instances."""
    
    def __init__(self, database_url: str = None):
        """
        Initialize database manager.
        
        Args:
            database_url: PostgreSQL connection URL (defaults to DATABASE_URL env var)
        """
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        # Create engine with connection pooling
        self.engine: Engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            echo=False,
        )
        
        # Load metadata
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        
        # Initialize repositories
        self.users = UsersRepository(self.engine, self.metadata)
        self.apartments = ApartmentsRepository(self.engine, self.metadata)
        self.meters = MetersRepository(self.engine, self.metadata)
        self.roles = UserRolesRepository(self.engine, self.metadata)
        self.readings = ReadingsRepository(self.engine, self.metadata)
        
        logger.info("Database manager initialized successfully")
    
    def health_check(self) -> bool:
        """
        Check if database connection is healthy.
        
        Returns:
            True if connection is OK, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            logger.info("Database health check passed")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def close(self) -> None:
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")
