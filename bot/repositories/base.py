"""
Base repository class for database access.
Uses SQLAlchemy Core for queries.
"""

from typing import Optional, List, Any
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base class for all repositories with common CRUD operations."""
    
    def __init__(self, engine: Engine, metadata: MetaData, table_name: str):
        """
        Initialize repository.
        
        Args:
            engine: SQLAlchemy engine
            metadata: SQLAlchemy metadata object
            table_name: Name of the table this repository manages
        """
        self.engine = engine
        self.metadata = metadata
        self.table: Table = metadata.tables[table_name]
    
    def insert(self, values: dict) -> Optional[Any]:
        """
        Insert a row into the table.
        
        Args:
            values: Dictionary of column names to values
        
        Returns:
            Result of insert operation
        """
        try:
            stmt = insert(self.table).values(**values)
            with self.engine.begin() as conn:
                result = conn.execute(stmt)
                conn.commit()
            logger.info(f"Inserted row into {self.table.name}: {values}")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error inserting into {self.table.name}: {e}")
            raise
    
    def select_by_id(self, row_id: int) -> Optional[dict]:
        """Select a row by ID."""
        try:
            stmt = select(self.table).where(self.table.c.id == row_id)
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error selecting from {self.table.name}: {e}")
            raise
    
    def select_all(self) -> List[dict]:
        """Select all rows from the table."""
        try:
            stmt = select(self.table)
            with self.engine.connect() as conn:
                results = conn.execute(stmt).fetchall()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            logger.error(f"Error selecting all from {self.table.name}: {e}")
            raise
    
    def update_by_id(self, row_id: int, values: dict) -> None:
        """Update a row by ID."""
        try:
            stmt = update(self.table).where(self.table.c.id == row_id).values(**values)
            with self.engine.begin() as conn:
                conn.execute(stmt)
                conn.commit()
            logger.info(f"Updated row {row_id} in {self.table.name}")
        except SQLAlchemyError as e:
            logger.error(f"Error updating {self.table.name}: {e}")
            raise
    
    def delete_by_id(self, row_id: int) -> None:
        """Delete a row by ID."""
        try:
            stmt = delete(self.table).where(self.table.c.id == row_id)
            with self.engine.begin() as conn:
                conn.execute(stmt)
                conn.commit()
            logger.info(f"Deleted row {row_id} from {self.table.name}")
        except SQLAlchemyError as e:
            logger.error(f"Error deleting from {self.table.name}: {e}")
            raise
