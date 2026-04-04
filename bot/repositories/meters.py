"""
Meters repository for database access to meters table.
"""

from typing import Optional, List
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class MetersRepository(BaseRepository):
    """Repository for meter management (meters table)."""
    
    def __init__(self, engine: Engine, metadata):
        """Initialize meters repository."""
        super().__init__(engine, metadata, 'meters')
    
    def create_meter(self, apartment_id: int, meter_number: str, 
                    installed_at: date = None) -> dict:
        """
        Create a new meter.
        
        Args:
            apartment_id: Apartment ID this meter belongs to
            meter_number: Physical meter serial/ID
            installed_at: Installation date
        
        Returns:
            Created meter dict
        """
        values = {
            'apartment_id': apartment_id,
            'meter_number': meter_number,
            'installed_at': installed_at,
            'is_active': True,
        }
        self.insert(values)
        
        # Fetch the newly created meter
        stmt = select(self.table).where(self.table.c.meter_number == meter_number)
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
        return dict(result._mapping) if result else None
    
    def get_by_meter_number(self, meter_number: str) -> Optional[dict]:
        """Get meter by meter number."""
        try:
            stmt = select(self.table).where(self.table.c.meter_number == meter_number)
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting meter {meter_number}: {e}")
            raise
    
    def get_meters_for_apartment(self, apartment_id: int) -> List[dict]:
        """
        Get all active meters for an apartment.
        
        Args:
            apartment_id: Apartment ID
        
        Returns:
            List of meter dicts
        """
        try:
            stmt = select(self.table).where(
                and_(
                    self.table.c.apartment_id == apartment_id,
                    self.table.c.is_active == True
                )
            )
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting meters for apartment {apartment_id}: {e}")
            raise
    
    def deactivate_meter(self, meter_id: int) -> None:
        """Deactivate a meter."""
        self.update_by_id(meter_id, {'is_active': False})
