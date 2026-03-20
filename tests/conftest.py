import os

import pytest
import pytest_asyncio
from httpx import AsyncClient
from tortoise.contrib.test import tortoise_test_context


# @pytest.fixture(
@pytest_asyncio.fixture(scope="session", autouse=True)
async def db():
    """Provide isolated database context for each test."""
    db_url = os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:")
    async with tortoise_test_context(["app.models"], db_url=db_url) as ctx:
        yield ctx


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client
