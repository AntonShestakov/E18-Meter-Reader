"""
Roles service — business logic for role management.

Handles:
- Role assignment / revocation
- Role validation
- Permission checks
- Time-scoped role validity
"""

import logging
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple

from bot.models import UserRole
from bot.repositories.roles import UserRolesRepository
from bot.repositories.users import UsersRepository

logger = logging.getLogger(__name__)

# Role privilege hierarchy (higher number = more privilege)
ROLE_HIERARCHY = {
    "tenant": 1,
    "grayhound": 2,
    "administrator": 3,
}


class RoleService:
    """
    Business logic for user roles and permissions.
    """

    def __init__(self, roles_repo: UserRolesRepository, users_repo: UsersRepository):
        """
        Initialize role service.

        Args:
            roles_repo: Repository for role CRUD
            users_repo: Repository for user lookups
        """
        self.roles_repo = roles_repo
        self.users_repo = users_repo

    async def assign_role(
        self,
        user_id: int,
        role: str,
        apartment_id: Optional[int] = None,
        valid_from: Optional[date] = None,
        valid_to: Optional[date] = None,
        assigned_by: Optional[int] = None,
    ) -> UserRole:
        """
        Assign a role to a user.

        Args:
            user_id: User ID
            role: Role name ('tenant', 'grayhound', 'administrator')
            apartment_id: Apartment ID (required for tenant/grayhound)
            valid_from: Start date (default: today)
            valid_to: End date (default: None = indefinite)
            assigned_by: Admin user ID assigning the role

        Returns:
            Created UserRole instance

        Raises:
            ValueError: If role/user invalid or duplicate assignment
        """
        if role not in ROLE_HIERARCHY:
            raise ValueError(f"Invalid role: {role}")

        # Validate user exists
        user = await self.users_repo.get_by_telegram_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Validate tenant/grayhound requires apartment
        if role in ("tenant", "grayhound") and not apartment_id:
            raise ValueError(f"Role '{role}' requires apartment_id")

        # Set defaults
        if valid_from is None:
            valid_from = date.today()

        # Check for duplicate active role
        active_roles = await self.roles_repo.get_active_roles(user_id)
        if any(r.role == role for r in active_roles):
            raise ValueError(f"User {user_id} already has role '{role}'")

        try:
            role_assignment = await self.roles_repo.assign_role(
                user_id=user_id,
                role=role,
                apartment_id=apartment_id,
                valid_from=valid_from,
                valid_to=valid_to,
                assigned_by=assigned_by,
            )
            logger.info(f"Role assigned: user={user_id}, role={role}, apt={apartment_id}")
            return role_assignment
        except Exception as e:
            logger.error(f"Failed to assign role: {e}")
            raise

    async def revoke_role(
        self, user_id: int, role: str, revoked_by: Optional[int] = None
    ) -> None:
        """
        Revoke a role from a user.

        Args:
            user_id: User ID
            role: Role name
            revoked_by: Admin user ID (for audit)

        Raises:
            ValueError: If role not found
        """
        try:
            await self.roles_repo.revoke_role(user_id, role)
            logger.info(f"Role revoked: user={user_id}, role={role}, by={revoked_by}")
        except Exception as e:
            logger.error(f"Failed to revoke role: {e}")
            raise

    async def get_active_roles(self, user_id: int) -> List[UserRole]:
        """
        Get all active roles for a user at current date.

        Args:
            user_id: User ID

        Returns:
            List of active UserRole instances
        """
        try:
            return await self.roles_repo.get_active_roles(user_id, check_date=date.today())
        except Exception as e:
            logger.error(f"Failed to fetch active roles for user {user_id}: {e}")
            raise

    async def get_highest_privilege_role(self, user_id: int) -> Optional[str]:
        """
        Get the highest-privilege role for a user.

        Args:
            user_id: User ID

        Returns:
            Role name ('tenant', 'grayhound', 'administrator') or None
        """
        try:
            active_roles = await self.get_active_roles(user_id)
            if not active_roles:
                return None

            # Find role with highest privilege
            highest = max(active_roles, key=lambda r: ROLE_HIERARCHY.get(r.role, 0))
            return highest.role
        except Exception as e:
            logger.error(f"Failed to determine highest privilege role for user {user_id}: {e}")
            raise

    async def has_permission(self, user_id: int, required_role: str) -> bool:
        """
        Check if user has minimum required role privilege.

        Args:
            user_id: User ID
            required_role: Minimum role required

        Returns:
            True if user's highest role >= required_role, False otherwise
        """
        try:
            highest_role = await self.get_highest_privilege_role(user_id)
            if not highest_role:
                return False

            user_privilege = ROLE_HIERARCHY.get(highest_role, 0)
            required_privilege = ROLE_HIERARCHY.get(required_role, 0)
            return user_privilege >= required_privilege
        except Exception as e:
            logger.error(f"Failed to check permissions for user {user_id}: {e}")
            raise

    async def get_users_for_apartment(self, apartment_id: int) -> List[Tuple[int, str]]:
        """
        Get all active users for an apartment (tenants/grayhounds).

        Args:
            apartment_id: Apartment ID

        Returns:
            List of (user_id, role) tuples
        """
        try:
            # TODO: Implement query to get active users for apartment
            return []
        except Exception as e:
            logger.error(f"Failed to fetch users for apartment {apartment_id}: {e}")
            raise
