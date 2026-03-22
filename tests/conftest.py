import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient, ASGITransport
from tortoise.contrib.test import tortoise_test_context

from app.core.settings import TestSettings
from app.domain.enums.task_status import TaskStatus
from app.main import app
from app.models.task_model import Task

fake = Faker()


@pytest_asyncio.fixture(autouse=True)
async def db():
    settings = TestSettings()

    async with tortoise_test_context(settings.APP_MODELS):
        yield


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    def _get_test_settings():
        return TestSettings()

    monkeypatch.setattr("app.core.settings.get_settings", _get_test_settings)


@pytest.fixture
async def task_factory():
    async def _create(**kwargs):
        data = {
            "title": fake.sentence(),
            "description": fake.text(),
            "status": TaskStatus.PENDING,
            **kwargs
        }
        return await Task.create(**data)

    return _create
