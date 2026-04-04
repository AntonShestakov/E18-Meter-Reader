"""
Repository module exports.
Provides easy access to all database repositories.
"""

from .users import UsersRepository
from .apartments import ApartmentsRepository
from .meters import MetersRepository
from .roles import UserRolesRepository
from .readings import ReadingsRepository

__all__ = [
    "UsersRepository",
    "ApartmentsRepository",
    "MetersRepository",
    "UserRolesRepository",
    "ReadingsRepository",
]
