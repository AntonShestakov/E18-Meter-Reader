"""
Users repository for Tortoise ORM User model.
"""

from typing import Optional, List
from bot.models import User
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UsersRepository(BaseRepository):
    """Repository for user accounts."""

    def __init__(self):
        """Initialize users repository."""
        super().__init__(User)

    async def get_by_telegram_id(self, user_id: int) -> Optional[User]:
        """
        Get user by Telegram user ID.

        Args:
            user_id: Telegram user ID (primary key)

        Returns:
            User instance or None
        """
        try:
            return await User.get_or_none(id=user_id)
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise

    async def create_user(
        self, user_id: int, username: str = None, full_name: str = None
    ) -> User:
        """
        Create a new user.

        Args:
            user_id: Telegram user ID
            username: Telegram username (optional)
            full_name: User's full name

        Returns:
            Created User instance
        """
        return await self.create(
            id=user_id,
            username=username,
            full_name=full_name,
            is_active=True,
        )

    async def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user (soft delete)."""
        return await self.update(user_id, is_active=False)

    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        try:
            return await User.filter(is_active=True).all()
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            raise
