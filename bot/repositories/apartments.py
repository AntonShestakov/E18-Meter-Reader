"""
Apartments repository for Tortoise ORM Apartment model.
"""

from typing import Optional, List
from bot.models import Apartment
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class ApartmentsRepository(BaseRepository):
    """Repository for apartment management."""
    
    def __init__(self):
        """Initialize apartments repository."""
        super().__init__(Apartment)
    
    async def get_by_number(self, number: str) -> Optional[Apartment]:
        """
        Get apartment by apartment number.
        
        Args:
            number: Apartment number (e.g., "42", "42A")
        
        Returns:
            Apartment instance or None
        """
        try:
            return await Apartment.get_or_none(number=number)
        except Exception as e:
            logger.error(f"Error getting apartment {number}: {e}")
            raise
    
    async def create_apartment(self, number: str, floor: int = None, notes: str = None) -> Apartment:
        """
        Create a new apartment.
        
        Args:
            number: Apartment number
            floor: Floor number (optional)
            notes: Additional notes (optional)
        
        Returns:
            Created Apartment instance
        """
        return await self.create(
            number=number,
            floor=floor,
            notes=notes,
        )
    
    async def get_all_apartments(self) -> List[Apartment]:
        """Get all apartments ordered by number."""
        try:
            return await Apartment.all().order_by('number')
        except Exception as e:
            logger.error(f"Error getting all apartments: {e}")
            raise

