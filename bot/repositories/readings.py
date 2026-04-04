"""
Readings repository for database access to readings table.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class ReadingsRepository(BaseRepository):
    """Repository for meter readings (readings table)."""
    
    def __init__(self, engine: Engine, metadata):
        """Initialize readings repository."""
        super().__init__(engine, metadata, 'readings')
    
    def create_reading(self, meter_id: int, value: float, submitted_by: int,
                      source: str = 'numeric', photo_file_id: str = None,
                      notes: str = None) -> dict:
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
            Created reading dict
        """
        values = {
            'meter_id': meter_id,
            'value': value,
            'submitted_by': submitted_by,
            'source': source,
            'photo_file_id': photo_file_id,
            'notes': notes,
        }
        self.insert(values)
        
        # Fetch the newly created reading
        stmt = select(self.table).where(
            and_(
                self.table.c.meter_id == meter_id,
                self.table.c.submitted_by == submitted_by
            )
        ).order_by(self.table.c.read_at.desc())
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
        return dict(result._mapping) if result else None
    
    def get_readings_for_apartment(self, apartment_id: int) -> List[dict]:
        """
        Get all readings for an apartment.
        
        Args:
            apartment_id: Apartment ID
        
        Returns:
            List of readings
        """
        try:
            # Join with meters table to filter by apartment
            from sqlalchemy import join
            meters_table = self.metadata.tables['meters']
            stmt = select(self.table).join(
                meters_table,
                self.table.c.meter_id == meters_table.c.id
            ).where(
                meters_table.c.apartment_id == apartment_id
            ).order_by(self.table.c.read_at.desc())
            
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting readings for apartment {apartment_id}: {e}")
            raise
    
    def get_readings_for_user(self, user_id: int) -> List[dict]:
        """
        Get all readings submitted by a user.
        
        Args:
            user_id: User ID (submitted_by)
        
        Returns:
            List of readings
        """
        try:
            stmt = select(self.table).where(
                self.table.c.submitted_by == user_id
            ).order_by(self.table.c.read_at.desc())
            
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting readings for user {user_id}: {e}")
            raise
    
    def get_latest_reading_for_meter(self, meter_id: int) -> Optional[dict]:
        """
        Get the latest reading for a specific meter.
        
        Args:
            meter_id: Meter ID
        
        Returns:
            Latest reading dict or None
        """
        try:
            stmt = select(self.table).where(
                self.table.c.meter_id == meter_id
            ).order_by(self.table.c.read_at.desc()).limit(1)
            
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting latest reading for meter {meter_id}: {e}")
            raise
