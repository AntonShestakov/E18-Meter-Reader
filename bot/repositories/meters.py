"""
Meters repository for Tortoise ORM Meter model.
"""

from typing import Optional, List
from datetime import date
from bot.models import Meter
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class MetersRepository(BaseRepository):
    """Repository for meter management."""

    def __init__(self):
        """Initialize meters repository."""
        super().__init__(Meter)

    async def create_meter(
        self, apartment_id: int, meter_number: str, installed_at: date = None
    ) -> Meter:
        """
        Create a new meter.

        Args:
            apartment_id: Apartment ID this meter belongs to
            meter_number: Physical meter serial/ID
            installed_at: Installation date

        Returns:
            Created Meter instance
        """
        return await self.create(
            apartment_id=apartment_id,
            meter_number=meter_number,
            installed_at=installed_at,
            is_active=True,
        )

    async def get_by_meter_number(self, meter_number: str) -> Optional[Meter]:
        """Get meter by meter number."""
        try:
            return await Meter.get_or_none(meter_number=meter_number)
        except Exception as e:
            logger.error(f"Error getting meter {meter_number}: {e}")
            raise

    async def get_meters_for_apartment(self, apartment_id: int) -> List[Meter]:
        """
        Get all active meters for an apartment.

        Args:
            apartment_id: Apartment ID

        Returns:
            List of Meter instances
        """
        try:
            return await Meter.filter(apartment_id=apartment_id, is_active=True).all()
        except Exception as e:
            logger.error(f"Error getting meters for apartment {apartment_id}: {e}")
            raise

    async def deactivate_meter(self, meter_id: int) -> Optional[Meter]:
        """Deactivate a meter."""
        return await self.update(meter_id, is_active=False)
