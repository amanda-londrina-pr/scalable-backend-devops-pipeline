import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_list_tasks_endpoint_status_code_ok(async_client: AsyncClient):
    response = await async_client.get("/tasks/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_tasks_endpoint_body(async_client: AsyncClient):
    response = await async_client.get("/tasks/")
    assert response.json() == []
