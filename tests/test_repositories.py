"""
Tests for repository layer classes.
"""

import pytest
from datetime import date
from unittest.mock import MagicMock, patch
from bot.repositories import (
    UsersRepository,
    ApartmentsRepository,
    MetersRepository,
    UserRolesRepository,
    ReadingsRepository,
)


@pytest.fixture
def mock_engine():
    """Create a mock SQLAlchemy engine."""
    return MagicMock()


@pytest.fixture
def mock_metadata():
    """Create a mock metadata object with tables."""
    metadata = MagicMock()
    
    # Create mock tables
    metadata.tables = {
        'users': MagicMock(name='users'),
        'apartments': MagicMock(name='apartments'),
        'meters': MagicMock(name='meters'),
        'user_roles': MagicMock(name='user_roles'),
        'readings': MagicMock(name='readings'),
    }
    
    return metadata


def test_users_repository_init(mock_engine, mock_metadata):
    """Test UsersRepository initialization."""
    repo = UsersRepository(mock_engine, mock_metadata)
    
    assert repo.engine == mock_engine
    assert repo.metadata == mock_metadata
    assert repo.table == mock_metadata.tables['users']


def test_apartments_repository_init(mock_engine, mock_metadata):
    """Test ApartmentsRepository initialization."""
    repo = ApartmentsRepository(mock_engine, mock_metadata)
    
    assert repo.engine == mock_engine
    assert repo.table == mock_metadata.tables['apartments']


def test_user_roles_repository_init(mock_engine, mock_metadata):
    """Test UserRolesRepository initialization."""
    repo = UserRolesRepository(mock_engine, mock_metadata)
    
    assert repo.engine == mock_engine
    assert repo.table == mock_metadata.tables['user_roles']


def test_meters_repository_init(mock_engine, mock_metadata):
    """Test MetersRepository initialization."""
    repo = MetersRepository(mock_engine, mock_metadata)
    
    assert repo.engine == mock_engine
    assert repo.table == mock_metadata.tables['meters']


def test_readings_repository_init(mock_engine, mock_metadata):
    """Test ReadingsRepository initialization."""
    repo = ReadingsRepository(mock_engine, mock_metadata)
    
    assert repo.engine == mock_engine
    assert repo.table == mock_metadata.tables['readings']


def test_user_roles_get_highest_privilege_role(mock_engine, mock_metadata):
    """Test getting highest privilege role when user has multiple roles."""
    repo = UserRolesRepository(mock_engine, mock_metadata)
    
    # Mock the get_active_roles method
    repo.get_active_roles = MagicMock(return_value=[
        {'role': 'grayhound'},
        {'role': 'tenant'},
    ])
    
    # Test that grayhound is returned (higher privilege than tenant)
    highest_role = repo.get_highest_privilege_role(123)
    assert highest_role == 'grayhound'


def test_user_roles_get_highest_privilege_administrator(mock_engine, mock_metadata):
    """Test that administrator role is highest privilege."""
    repo = UserRolesRepository(mock_engine, mock_metadata)
    
    # Mock roles including administrator
    repo.get_active_roles = MagicMock(return_value=[
        {'role': 'administrator'},
        {'role': 'grayhound'},
        {'role': 'tenant'},
    ])
    
    highest_role = repo.get_highest_privilege_role(123)
    assert highest_role == 'administrator'


def test_user_roles_get_highest_privilege_no_roles(mock_engine, mock_metadata):
    """Test getting highest privilege role when user has no active roles."""
    repo = UserRolesRepository(mock_engine, mock_metadata)
    
    repo.get_active_roles = MagicMock(return_value=[])
    
    highest_role = repo.get_highest_privilege_role(123)
    assert highest_role is None
