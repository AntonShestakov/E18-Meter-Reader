"""
Readings repository for Tortoise ORM Reading model.
"""

from typing import Optional, List
from bot.models import Reading
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class ReadingsRepository(BaseRepository):
    """Repository for meter readings."""

    def __init__(self):
        """Initialize readings repository."""
        super().__init__(Reading)

    async def create_reading(
        self,
        meter_id: int,
        value: float,
        submitted_by: int,
        source: str = "numeric",
        photo_file_id: str = None,
        notes: str = None,
    ) -> Reading:
        """
        Create a new meter reading.

        Args:
            meter_id: Meter ID
            value: Reading value (kWh)
            submitted_by: User ID who submitted the reading
            source: 'numeric' or 'photo'
            photo_file_id: Telegram file ID if source is photo
            notes: Optional notes

        Returns:
            Created Reading instance
        """
        return await self.create(
            meter_id=meter_id,
            value=value,
            submitted_by=submitted_by,
            source=source,
            photo_file_id=photo_file_id,
            notes=notes,
        )

    async def get_readings_for_apartment(self, apartment_id: int) -> List[Reading]:
        """
        Get all readings for an apartment.

        Args:
            apartment_id: Apartment ID

        Returns:
            List of Reading instances
        """
        try:
            # Filter readings by apartment through meters
            return (
                await Reading.filter(meter__apartment_id=apartment_id)
                .order_by("-read_at")
                .all()
            )
        except Exception as e:
            logger.error(f"Error getting readings for apartment {apartment_id}: {e}")
            raise

    async def get_readings_for_user(self, user_id: int) -> List[Reading]:
        """
        Get all readings submitted by a user.

        Args:
            user_id: User ID (submitted_by)

        Returns:
            List of Reading instances
        """
        try:
            return await Reading.filter(submitted_by=user_id).order_by("-read_at").all()
        except Exception as e:
            logger.error(f"Error getting readings for user {user_id}: {e}")
            raise

    async def get_latest_reading_for_meter(self, meter_id: int) -> Optional[Reading]:
        """
        Get the latest reading for a specific meter.

        Args:
            meter_id: Meter ID

        Returns:
            Latest Reading instance or None
        """
        try:
            return await Reading.filter(meter_id=meter_id).order_by("-read_at").first()
        except Exception as e:
            logger.error(f"Error getting latest reading for meter {meter_id}: {e}")
            raise
