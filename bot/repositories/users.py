"""
Users repository for database access to users table.
"""

from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UsersRepository(BaseRepository):
    """Repository for user accounts (users table)."""
    
    def __init__(self, engine: Engine, metadata):
        """Initialize users repository."""
        super().__init__(engine, metadata, 'users')
    
    def get_by_telegram_id(self, user_id: int) -> Optional[dict]:
        """
        Get user by Telegram user ID.
        
        Args:
            user_id: Telegram user ID (primary key)
        
        Returns:
            User dict or None if not found
        """
        try:
            stmt = select(self.table).where(self.table.c.id == user_id)
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise
    
    def create_user(self, user_id: int, username: str = None, full_name: str = None) -> dict:
        """
        Create a new user.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username (optional)
            full_name: User's full name
        
        Returns:
            Created user dict
        """
        values = {
            'id': user_id,
            'username': username,
            'full_name': full_name,
            'is_active': True,
        }
        self.insert(values)
        return self.get_by_telegram_id(user_id)
    
    def deactivate_user(self, user_id: int) -> None:
        """Deactivate a user (soft delete)."""
        self.update_by_id(user_id, {'is_active': False})
    
    def get_active_users(self) -> list:
        """Get all active users."""
        try:
            stmt = select(self.table).where(self.table.c.is_active == True)
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting active users: {e}")
            raise
