"""
User roles repository for Tortoise ORM UserRole model.
Handles role assignments with time-scoped validity.
"""

from typing import Optional, List
from datetime import date
from bot.models import UserRole
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UserRolesRepository(BaseRepository):
    """Repository for user role assignments."""
    
    def __init__(self):
        """Initialize user_roles repository."""
        super().__init__(UserRole)
    
    async def assign_role(self, user_id: int, role: str, valid_from: date, 
                         valid_to: date = None, apartment_id: int = None, 
                         assigned_by: int = None) -> UserRole:
        """
        Assign a role to a user.
        
        Args:
            user_id: User ID (Telegram ID)
            role: Role name ('administrator', 'grayhound', 'tenant')
            valid_from: Start date for role validity
            valid_to: End date for role validity (None = indefinite)
            apartment_id: Apartment ID (required for tenant role)
            assigned_by: Administrator user ID who made this assignment
        
        Returns:
            Created UserRole instance
        """
        return await self.create(
            user_id=user_id,
            role=role,
            valid_from=valid_from,
            valid_to=valid_to,
            apartment_id=apartment_id,
            assigned_by=assigned_by,
        )
    
    async def get_active_roles(self, user_id: int, check_date: date = None) -> List[UserRole]:
        """
        Get all active roles for a user.
        
        Args:
            user_id: User ID
            check_date: Date to check validity against (default: today)
        
        Returns:
            List of active UserRole instances
        """
        if check_date is None:
            check_date = date.today()
        
        try:
            # Get roles where valid_from <= check_date AND (valid_to >= check_date OR valid_to is NULL)
            all_roles = await UserRole.filter(
                user_id=user_id,
                valid_from__lte=check_date,
            ).all()
            
            # Filter in memory for valid_to condition (valid_to is None or valid_to >= check_date)
            active = [r for r in all_roles if r.valid_to is None or r.valid_to >= check_date]
            return active
        except Exception as e:
            logger.error(f"Error getting active roles for user {user_id}: {e}")
            raise
    
    async def get_highest_privilege_role(self, user_id: int) -> Optional[str]:
        """
        Get the highest-privilege active role for a user.
        Privilege order: administrator > grayhound > tenant
        
        Args:
            user_id: User ID
        
        Returns:
            Role name string or None
        """
        active_roles = await self.get_active_roles(user_id)
        if not active_roles:
            return None
        
        role_names = [r.role for r in active_roles]
        
        # Privilege order
        if 'administrator' in role_names:
            return 'administrator'
        elif 'grayhound' in role_names:
            return 'grayhound'
        elif 'tenant' in role_names:
            return 'tenant'
        
        return None
    
    async def revoke_role(self, user_id: int, role: str) -> None:
        """Revoke a role from a user."""
        try:
            await UserRole.filter(user_id=user_id, role=role).delete()
            logger.info(f"Revoked {role} role from user {user_id}")
        except Exception as e:
            logger.error(f"Error revoking role: {e}")
            raise


