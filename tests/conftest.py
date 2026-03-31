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


@pytest_asyncio.fixture
async def created_task_id(async_client):
    response = await async_client.post("/tasks/", json={
        "title": "Test",
        "description": "Description"
    })
    task_id = response.json().get("id", None)
    yield task_id
    await async_client.delete(f"/tasks/{task_id}")


@pytest_asyncio.fixture
async def completed_task_id(async_client, created_task_id):
    await async_client.patch(f"/tasks/{created_task_id}/complete")
    yield created_task_id


@pytest_asyncio.fixture
def task_factory():
    async def _create(**kwargs):
        task = await Task.create(
            title=kwargs.get("title", fake.sentence()),
            description=kwargs.get("description", fake.text()),
            status=kwargs.get("status", TaskStatus.PENDING),
        )
        return task

    return _create
