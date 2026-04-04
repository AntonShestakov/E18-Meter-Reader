"""
User roles repository for database access to user_roles table.
Handles role assignments with time-scoped validity.
"""

from typing import Optional, List
from datetime import date
from sqlalchemy import select, and_, or_, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UserRolesRepository(BaseRepository):
    """Repository for user role assignments (user_roles table)."""
    
    def __init__(self, engine: Engine, metadata):
        """Initialize user_roles repository."""
        super().__init__(engine, metadata, 'user_roles')
    
    def assign_role(self, user_id: int, role: str, valid_from: date, 
                   valid_to: date = None, apartment_id: int = None, 
                   assigned_by: int = None) -> dict:
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
            Created role assignment dict
        """
        values = {
            'user_id': user_id,
            'role': role,
            'valid_from': valid_from,
            'valid_to': valid_to,
            'apartment_id': apartment_id,
            'assigned_by': assigned_by,
        }
        self.insert(values)
        
        # Fetch the newly created role
        stmt = select(self.table).where(
            and_(
                self.table.c.user_id == user_id,
                self.table.c.role == role,
                self.table.c.valid_from == valid_from
            )
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
        return dict(result._mapping) if result else None
    
    def get_active_roles(self, user_id: int, check_date: date = None) -> List[dict]:
        """
        Get all active roles for a user.
        
        Args:
            user_id: User ID
            check_date: Date to check validity against (default: today)
        
        Returns:
            List of active role dicts
        """
        if check_date is None:
            check_date = date.today()
        
        try:
            stmt = select(self.table).where(
                and_(
                    self.table.c.user_id == user_id,
                    self.table.c.valid_from <= check_date,
                    or_(
                        self.table.c.valid_to == None,
                        self.table.c.valid_to >= check_date
                    )
                )
            )
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting active roles for user {user_id}: {e}")
            raise
    
    def get_highest_privilege_role(self, user_id: int) -> Optional[str]:
        """
        Get the highest-privilege active role for a user.
        Privilege order: administrator > grayhound > tenant
        
        Args:
            user_id: User ID
        
        Returns:
            Role name string or None
        """
        active_roles = self.get_active_roles(user_id)
        if not active_roles:
            return None
        
        role_names = [r['role'] for r in active_roles]
        
        # Privilege order
        if 'administrator' in role_names:
            return 'administrator'
        elif 'grayhound' in role_names:
            return 'grayhound'
        elif 'tenant' in role_names:
            return 'tenant'
        
        return None
    
    def revoke_role(self, user_id: int, role: str) -> None:
        """Revoke a role from a user."""
        try:
            stmt = delete(self.table).where(
                and_(
                    self.table.c.user_id == user_id,
                    self.table.c.role == role
                )
            )
            with self.engine.begin() as conn:
                conn.execute(stmt)
                conn.commit()
            logger.info(f"Revoked {role} role from user {user_id}")
        except SQLAlchemyError as e:
            logger.error(f"Error revoking role: {e}")
            raise
