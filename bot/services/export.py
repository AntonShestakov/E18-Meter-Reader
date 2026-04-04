"""
Export service — business logic for reading exports.

Handles:
- CSV export of readings
- Filtering by date range and apartment
- Permission-based access (tenant sees own only, grayhound/admin see building)
"""

import logging
import csv
import io
from datetime import date, timedelta
from typing import List, Optional

from bot.models import Reading
from bot.repositories.readings import ReadingsRepository
from bot.repositories.apartments import ApartmentsRepository
from bot.services.roles import RoleService

logger = logging.getLogger(__name__)


class ExportService:
    """
    Business logic for exporting readings to various formats.
    """

    def __init__(
        self,
        readings_repo: ReadingsRepository,
        apartments_repo: ApartmentsRepository,
        roles_service: RoleService,
    ):
        """
        Initialize export service.

        Args:
            readings_repo: Repository for reading CRUD
            apartments_repo: Repository for apartment lookups
            roles_service: Service for permission checks
        """
        self.readings_repo = readings_repo
        self.apartments_repo = apartments_repo
        self.roles_service = roles_service

    async def export_readings_csv(
        self,
        user_id: int,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        apartment_id: Optional[int] = None,
    ) -> str:
        """
        Export readings to CSV format.

        Permissions:
        - Tenant: Can only export their own apartment readings
        - Grayhound: Can export any apartment in building
        - Administrator: Can export any apartment

        Args:
            user_id: Requesting user ID
            date_from: Start date (default: 30 days ago)
            date_to: End date (default: today)
            apartment_id: Specific apartment (optional filter)

        Returns:
            CSV content as string

        Raises:
            PermissionError: If user lacks permission
            ValueError: If parameters invalid
        """
        try:
            # Check minimum permission (tenant role)
            has_access = await self.roles_service.has_permission(user_id, "tenant")
            if not has_access:
                raise PermissionError("You don't have permission to export readings")

            # Set date range defaults
            if date_to is None:
                date_to = date.today()
            if date_from is None:
                date_from = date_to - timedelta(days=30)

            if date_from > date_to:
                raise ValueError("date_from must be before date_to")

            # Get readings based on user role and filters
            readings = await self._get_filtered_readings(
                user_id, date_from, date_to, apartment_id
            )

            # Generate CSV
            csv_content = self._generate_csv(readings)
            logger.info(
                f"CSV export: user={user_id}, {len(readings)} readings, "
                f"period={date_from} to {date_to}"
            )
            return csv_content

        except PermissionError:
            raise
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            raise

    async def _get_filtered_readings(
        self,
        user_id: int,
        date_from: date,
        date_to: date,
        apartment_id: Optional[int] = None,
    ) -> List[Reading]:
        """
        Get readings filtered by user role and optional apartment.

        Args:
            user_id: User requesting export
            date_from: Start date
            date_to: End date
            apartment_id: Optional apartment filter

        Returns:
            List of filtered Reading instances
        """
        # Get user's highest privilege role
        role = await self.roles_service.get_highest_privilege_role(user_id)

        readings = []

        if role == "tenant":
            # Tenant can only see apartment for which they have tenant role
            # TODO: Query to find user's apartment
            if apartment_id:
                readings = await self.readings_repo.get_readings_for_apartment(
                    apartment_id
                )
        elif role in ("grayhound", "administrator"):
            # Grayhound/Admin can see all apartments
            if apartment_id:
                readings = await self.readings_repo.get_readings_for_apartment(
                    apartment_id
                )
            else:
                # Get all apartments and their readings
                # TODO: Implement bulk reading fetch for all apartments
                pass

        # Filter by date range
        filtered = [r for r in readings if date_from <= r.read_at.date() <= date_to]
        return filtered

    @staticmethod
    def _generate_csv(readings: List[Reading]) -> str:
        """
        Generate CSV content from readings.

        Args:
            readings: List of Reading instances

        Returns:
            CSV content as string
        """
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(
            [
                "Date",
                "Time",
                "Apartment",
                "Meter Number",
                "Reading (kWh)",
                "Submitted By",
                "Source",
                "Notes",
            ]
        )

        # Write data rows
        for reading in readings:
            writer.writerow(
                [
                    reading.read_at.date().isoformat(),
                    reading.read_at.time().isoformat(),
                    reading.meter.apartment.number,  # TODO: Verify relationship
                    reading.meter.meter_number,
                    str(reading.value),
                    reading.submitted_by,
                    reading.source,
                    reading.notes or "",
                ]
            )

        return output.getvalue()

    async def validate_export_access(
        self, user_id: int, apartment_id: Optional[int] = None
    ) -> bool:
        """
        Check if user can export readings for apartment(s).

        Args:
            user_id: User ID
            apartment_id: Apartment to check (None = all)

        Returns:
            True if permitted, False otherwise
        """
        try:
            # Must have at least tenant role
            if not await self.roles_service.has_permission(user_id, "tenant"):
                return False

            # If apartment specified, verify access
            if apartment_id:
                role = await self.roles_service.get_highest_privilege_role(user_id)
                if role == "tenant":
                    # Tenant can only export own apartment
                    # TODO: Validate apartment matches user's apartment
                    pass

            return True
        except Exception as e:
            logger.error(f"Failed to validate export access: {e}")
            return False
