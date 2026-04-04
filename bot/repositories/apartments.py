"""
Apartments repository for database access to apartments table.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from .base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class ApartmentsRepository(BaseRepository):
    """Repository for apartment management (apartments table)."""
    
    def __init__(self, engine: Engine, metadata):
        """Initialize apartments repository."""
        super().__init__(engine, metadata, 'apartments')
    
    def get_by_number(self, number: str) -> Optional[dict]:
        """
        Get apartment by apartment number.
        
        Args:
            number: Apartment number (e.g., "42", "42A")
        
        Returns:
            Apartment dict or None if not found
        """
        try:
            stmt = select(self.table).where(self.table.c.number == number)
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error getting apartment {number}: {e}")
            raise
    
    def create_apartment(self, number: str, floor: int = None, notes: str = None) -> dict:
        """
        Create a new apartment.
        
        Args:
            number: Apartment number
            floor: Floor number (optional)
            notes: Additional notes (optional)
        
        Returns:
            Created apartment dict
        """
        values = {
            'number': number,
            'floor': floor,
            'notes': notes,
        }
        result = self.insert(values)
        # Fetch the newly created apartment
        stmt = select(self.table).where(self.table.c.number == number)
        with self.engine.connect() as conn:
            row = conn.execute(stmt).fetchone()
        return dict(row._mapping) if row else None
    
    def get_all_apartments(self) -> List[dict]:
        """Get all apartments ordered by number."""
        try:
            stmt = select(self.table).order_by(self.table.c.number)
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error getting all apartments: {e}")
            raise
