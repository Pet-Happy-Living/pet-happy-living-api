"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.api.common.client import APIClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_api_client():
    """Create a mock API client for testing."""
    client = APIClient("http://test.api.com")
    client._client = AsyncMock()
    return client


@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "status": "success",
        "data": {
            "id": 1,
            "name": "Test Data",
            "description": "Test description"
        }
    }


@pytest.fixture
def sample_error_response():
    """Sample error response for testing."""
    return {
        "error": "Bad Request",
        "message": "Invalid parameters",
        "status_code": 400
    } 