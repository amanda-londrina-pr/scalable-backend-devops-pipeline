import asyncio

import pytest
from fastapi import status

from app.domain.enums.task_status import TaskStatus
from app.services import task_service


@pytest.mark.asyncio
async def test_create_task_response_schema(async_client):
    response = await async_client.post("/tasks/", json={
        "title": "Test",
        "description": "Desc"
    })

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in data
    assert data["title"] == "Test"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_task_full_lifecycle(async_client):
    # create
    create = await async_client.post("/tasks/", json={
        "title": "Lifecycle test"
    })
    task_id = create.json()["id"]

    # initial state
    assert create.json()["status"] == TaskStatus.PENDING

    # complete
    complete = await async_client.patch(f"/tasks/{task_id}/complete")
    assert complete.json()["status"] == TaskStatus.DONE

    # reopen
    reopen = await async_client.patch(f"/tasks/{task_id}/reopen")
    assert reopen.json()["status"] == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_complete_task_success_integration(task_factory):
    task = await task_factory(status=TaskStatus.PENDING)
    result = await task_service.complete_task(task.id)
    assert result.status == TaskStatus.DONE


@pytest.mark.asyncio
async def test_create_task_with_invalid_status(async_client):
    create_response = await async_client.post("/tasks/", json={
        "title": "Test",
        "status": "status_auto_settled"
    })

    assert create_response.status_code == status.HTTP_201_CREATED


async def test_create_task_ignores_status(async_client):
    response = await async_client.post("/tasks/", json={
        "title": "Test",
        "status": "done"
    })

    assert response.status_code == 201
    assert response.json()["status"] == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_update_task_with_invalid_status(async_client, created_task_id):
    update_response = await async_client.put(f"/tasks/{created_task_id}", json={
        "status": "invalid_status"
    })

    assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_update_task_with_valid_description(async_client, created_task_id):
    update_response = await async_client.put(f"/tasks/{created_task_id}", json={
        "description": "Description updated"
    })

    assert update_response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_task_with_invalid_id(async_client):
    invalid_task_id = 1123
    update_response = await async_client.put(f"/tasks/{invalid_task_id}", json={
        "description": "Description updated"
    })

    assert update_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_complete_task(async_client, created_task_id):
    get_response = await async_client.get(f"/tasks/{created_task_id}")
    assert get_response.json()["status"] == TaskStatus.PENDING

    complete_response = await async_client.patch(f"/tasks/{created_task_id}/complete")
    assert complete_response.json()["status"] == TaskStatus.DONE


@pytest.mark.asyncio
async def test_invalid_reopen(async_client, completed_task_id):
    response = await async_client.patch(f"/tasks/{completed_task_id}/complete")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_invalid_transition_returns_400_bad_request(
        async_client,
        created_task_id):
    # PENDING → complete → DONE
    await async_client.patch(f"/tasks/{created_task_id}/complete")

    # DONE → complete again (invalid)
    response = await async_client.patch(f"/tasks/{created_task_id}/complete")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid status transition" in response.json()["detail"]


@pytest.mark.asyncio
async def test_complete_persists_in_db(async_client, created_task_id):
    await async_client.patch(f"/tasks/{created_task_id}/complete")

    response = await async_client.get(f"/tasks/{created_task_id}")

    assert response.json()["status"] == TaskStatus.DONE


@pytest.mark.asyncio
async def test_concurrent_complete(async_client, created_task_id):
    responses = await asyncio.gather(
        async_client.patch(f"/tasks/{created_task_id}/complete"),
        async_client.patch(f"/tasks/{created_task_id}/complete"),
    )

    statuses = [r.status_code for r in responses]

    assert status.HTTP_200_OK in statuses
    assert status.HTTP_400_BAD_REQUEST in statuses


async def test_concurrent_update(async_client, created_task_id):
    async def update():
        return await async_client.put(
            f"/tasks/{created_task_id}",
            json={"description": "update"}
        )

    responses = await asyncio.gather(update(), update())
    statuses = [r.status_code for r in responses]

    assert 200 in statuses
    assert 400 in statuses
