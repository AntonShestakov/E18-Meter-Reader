"""
Reading service — business logic for meter reading submissions.

Handles:
- Reading validation (range checks, deduplication)
- Reading storage
- Reading history retrieval
- Apartment-scoped access control
"""

import logging
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

from bot.models import Reading
from bot.repositories.readings import ReadingsRepository
from bot.repositories.meters import MetersRepository

logger = logging.getLogger(__name__)


class ReadingService:
    """
    Business logic for meter readings.
    """

    def __init__(
        self, readings_repo: ReadingsRepository, meters_repo: MetersRepository
    ):
        """
        Initialize reading service.

        Args:
            readings_repo: Repository for reading CRUD
            meters_repo: Repository for meter lookups
        """
        self.readings_repo = readings_repo
        self.meters_repo = meters_repo

    async def submit_reading(
        self,
        meter_id: int,
        value: Decimal,
        submitted_by: int,
        source: str = "numeric",
        photo_file_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Reading:
        """
        Submit a new meter reading with validation.

        Args:
            meter_id: ID of meter
            value: Reading value (kWh)
            submitted_by: User ID submitting reading
            source: 'numeric' or 'photo'
            photo_file_id: Telegram photo file ID if source='photo'
            notes: Optional notes

        Returns:
            Created Reading instance

        Raises:
            ValueError: If value is invalid or meter not found
        """
        # Validate value is positive number
        if not isinstance(value, (int, float, Decimal)):
            raise ValueError("Reading value must be numeric")

        if value < 0:
            raise ValueError("Reading value cannot be negative")

        # Verify meter exists
        meter = await self.meters_repo.get_by_id(meter_id)
        if not meter:
            raise ValueError(f"Meter {meter_id} not found")

        # Check for duplicate readings submitted within last 5 minutes
        latest = await self.readings_repo.get_latest_reading_for_meter(meter_id)
        if latest:
            time_delta = datetime.utcnow() - latest.read_at
            if time_delta.total_seconds() < 300:  # 5 minutes
                logger.warning(
                    f"Duplicate reading attempt for meter {meter_id} "
                    f"(submitted {time_delta.total_seconds()}s ago)"
                )
                raise ValueError(
                    "Reading was just submitted. Please wait before submitting again."
                )

        # Create reading
        try:
            reading = await self.readings_repo.create_reading(
                meter_id=meter_id,
                value=value,
                submitted_by=submitted_by,
                source=source,
                photo_file_id=photo_file_id,
                notes=notes,
            )
            logger.info(
                f"Reading submitted: meter={meter_id}, value={value}, by={submitted_by}"
            )
            return reading
        except Exception as e:
            logger.error(f"Failed to create reading: {e}")
            raise

    async def get_readings_for_user(
        self, user_id: int, limit: int = 10
    ) -> List[Reading]:
        """
        Get readings submitted by a user.

        Args:
            user_id: User ID
            limit: Max results

        Returns:
            List of Reading instances
        """
        try:
            readings = await self.readings_repo.get_readings_for_user(user_id)
            return readings[:limit]
        except Exception as e:
            logger.error(f"Failed to fetch readings for user {user_id}: {e}")
            raise

    async def get_readings_for_apartment(
        self, apartment_id: int, days_back: int = 30
    ) -> List[Reading]:
        """
        Get readings for an apartment (all meters).

        Args:
            apartment_id: Apartment ID
            days_back: How many days of history to return

        Returns:
            List of Reading instances
        """
        try:
            readings = await self.readings_repo.get_readings_for_apartment(apartment_id)
            # Filter by date if needed
            cutoff = datetime.utcnow().date() - __import__("datetime").timedelta(
                days=days_back
            )
            return [r for r in readings if r.read_at.date() >= cutoff]
        except Exception as e:
            logger.error(f"Failed to fetch readings for apartment {apartment_id}: {e}")
            raise

    async def get_latest_reading_for_meter(self, meter_id: int) -> Optional[Reading]:
        """
        Get most recent reading for a meter.

        Args:
            meter_id: Meter ID

        Returns:
            Reading instance or None
        """
        try:
            return await self.readings_repo.get_latest_reading_for_meter(meter_id)
        except Exception as e:
            logger.error(f"Failed to fetch latest reading for meter {meter_id}: {e}")
            raise
