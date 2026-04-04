"""
Base repository class for Tortoise ORM models.
Provides common async CRUD operations.
"""

import logging
from typing import List, Optional, TypeVar, Generic

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository with common async CRUD operations."""
    
    def __init__(self, model):
        """
        Initialize repository.
        
        Args:
            model: Tortoise ORM Model class
        """
        self.model = model
    
    async def create(self, **kwargs) -> T:
        """Create and return a new record."""
        try:
            instance = await self.model.create(**kwargs)
            logger.info(f"Created {self.model.__name__}: {instance}")
            return instance
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise
    
    async def get_by_id(self, id) -> Optional[T]:
        """Get record by ID."""
        try:
            return await self.model.get_or_none(id=id)
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by id {id}: {e}")
            raise
    
    async def get_all(self) -> List[T]:
        """Get all records."""
        try:
            return await self.model.all()
        except Exception as e:
            logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise
    
    async def update(self, id, **kwargs) -> Optional[T]:
        """Update record by ID."""
        try:
            instance = await self.get_by_id(id)
            if not instance:
                return None
            await instance.update_from_dict(kwargs)
            await instance.save()
            logger.info(f"Updated {self.model.__name__} {id}")
            return instance
        except Exception as e:
            logger.error(f"Error updating {self.model.__name__}: {e}")
            raise
    
    async def delete(self, id) -> bool:
        """Delete record by ID."""
        try:
            deleted = await self.model.filter(id=id).delete()
            if deleted:
                logger.info(f"Deleted {self.model.__name__} {id}")
            return bool(deleted)
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            raise

