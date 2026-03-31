from unittest.mock import AsyncMock, MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.domain.enums.task_status import TaskStatus
from app.domain.errors import NotFoundError, EmptyUpdateError, \
    InvalidStatusTransitionError
from app.services import task_service


# GET_BY_ID
@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_get_by_id_success(mock_task):
    fake_task = AsyncMock()
    mock_query = AsyncMock()
    mock_query.first = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value = mock_query

    result = await task_service.get_by_id(1)
    assert result == fake_task

    mock_task.filter.assert_called_once_with(id=1)
    mock_query.first.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_get_by_id_not_found(mock_task):
    mock_query = AsyncMock()
    mock_query.first = AsyncMock(return_value=None)
    mock_task.filter.return_value = mock_query

    with pytest.raises(NotFoundError):
        await task_service.get_by_id(1)

    mock_task.filter.assert_called_once_with(id=1)
    mock_query.first.assert_awaited_once()


# UPDATE
@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_empty_payload(mock_task):
    fake_task = AsyncMock()

    mock_task.get_or_none = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value.update = AsyncMock(return_value=1)

    data = Mock()
    data.to_orm.return_value = {}

    with pytest.raises(EmptyUpdateError):
        await task_service.update(1, data)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_success(mock_task):
    fake_task = AsyncMock()
    fake_task.version = 1

    # get_or_none
    mock_task.get_or_none = AsyncMock(return_value=fake_task)

    # update otimista
    mock_task.filter.return_value.update = AsyncMock(return_value=1)

    # get final
    mock_task.get = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "new title",
        "description": "new desc",
    }

    result = await task_service.update(1, data)

    assert result is not None
    mock_task.filter.return_value.update.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_not_found(mock_task):
    mock_task.get_or_none = AsyncMock(return_value=None)

    data = Mock()
    data.to_orm.return_value = {"title": "new"}

    with pytest.raises(NotFoundError):
        await task_service.update(1, data)

    mock_task.get_or_none.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_partial_fields(mock_task):
    fake_task = AsyncMock()
    fake_task.title = "old title"
    fake_task.description = "old desc"

    mock_task.get_or_none = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value.update = AsyncMock(return_value=1)
    mock_task.get = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "description": "new desc"
    }

    result = await task_service.update(1, data)

    assert result.title == "old title"
    assert result.description == "new desc"


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_concurrency_error(mock_task):
    fake_task = AsyncMock()
    fake_task.version = 1

    mock_task.get_or_none = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value.update = AsyncMock(return_value=0)

    data = Mock()
    data.to_orm.return_value = {"title": "new"}

    with pytest.raises(Exception):
        await task_service.update(1, data)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_calls_setattr(mock_task):
    fake_task = AsyncMock()

    mock_task.get_or_none = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value.update = AsyncMock(return_value=1)
    mock_task.get = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "new title",
    }

    await task_service.update(1, data)

    assert fake_task.title == "new title"


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_update_ignores_forbidden_fields(mock_task):
    fake_task = AsyncMock()
    fake_task.title = "old"
    fake_task.description = "old desc"

    mock_task.get_or_none = AsyncMock(return_value=fake_task)
    mock_task.filter.return_value.update = AsyncMock(return_value=1)
    mock_task.get = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "new title",
        "status": "SHOULD_BE_IGNORED",
    }

    result = await task_service.update(1, data)

    assert result.title == "new title"
    assert not hasattr(result, "status") or result.status != "SHOULD_BE_IGNORED"


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_create_success(mock_task):
    fake_task = AsyncMock()
    fake_task.id = 1

    mock_task.create = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "Test",
        "description": "Desc",
    }

    result = await task_service.create(data)

    assert result == fake_task

    mock_task.create.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_create_sets_status_pending(mock_task):
    fake_task = AsyncMock()
    mock_task.create = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "Test",
        "description": "Desc",
        "status": "SHOULD_BE_IGNORED"
    }

    await task_service.create(data)

    mock_task.create.assert_awaited_once_with(
        title="Test",
        description="Desc",
        status=TaskStatus.PENDING
    )


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_create_calls_to_orm(mock_task):
    fake_task = AsyncMock()
    mock_task.create = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "Test",
        "description": "Desc",
    }

    await task_service.create(data)

    data.to_orm.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_create_exact_payload(mock_task):
    fake_task = AsyncMock()
    mock_task.create = AsyncMock(return_value=fake_task)

    data = Mock()
    data.to_orm.return_value = {
        "title": "Test",
        "description": "Desc",
    }

    await task_service.create(data)

    args, kwargs = mock_task.create.await_args

    assert kwargs["title"] == "Test"
    assert kwargs["description"] == "Desc"
    assert kwargs["status"] == TaskStatus.PENDING


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_delete_success(mock_task):
    mock_query = AsyncMock()
    mock_query.delete = AsyncMock(return_value=1)

    mock_task.filter.return_value = mock_query

    result = await task_service.delete_by_id(1)

    assert result is None

    mock_task.filter.assert_called_once_with(id=1)
    mock_query.delete.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_delete_not_found(mock_task):
    mock_query = AsyncMock()
    mock_query.delete = AsyncMock(return_value=0)  # nada deletado

    mock_task.filter.return_value = mock_query

    with pytest.raises(NotFoundError):
        await task_service.delete_by_id(1)

    mock_task.filter.assert_called_once_with(id=1)
    mock_query.delete.assert_awaited_once()


# LIST_PAGINATED
@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_list_paginated_success(mock_task):
    fake_tasks = [MagicMock(), MagicMock()]

    # mock da query base
    mock_query = MagicMock()
    mock_query.count = AsyncMock(return_value=10)

    # encadeamento offset().limit()
    mock_query.offset.return_value.limit = AsyncMock(return_value=fake_tasks)

    mock_task.all.return_value = mock_query

    tasks, total, total_pages = await task_service.list_paginated(page=1, size=2)

    assert tasks == fake_tasks
    assert total == 10
    assert total_pages == 5  # 10 / 2

    mock_task.all.assert_called_once()
    mock_query.count.assert_awaited_once()
    mock_query.offset.assert_called_once_with(0)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_list_paginated_total_pages_round_up(mock_task):
    mock_query = MagicMock()
    mock_query.count = AsyncMock(return_value=9)

    mock_query.offset.return_value.limit = AsyncMock(return_value=[])

    mock_task.all.return_value = mock_query

    _, total, total_pages = await task_service.list_paginated(page=1, size=2)

    assert total == 9
    assert total_pages == 5  # (9 + 2 - 1) // 2


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_list_paginated_min_values(mock_task):
    mock_query = MagicMock()
    mock_query.count = AsyncMock(return_value=5)

    mock_query.offset.return_value.limit = AsyncMock(return_value=[])

    mock_task.all.return_value = mock_query

    await task_service.list_paginated(page=0, size=0)

    # page vira 1 → offset = 0
    mock_query.offset.assert_called_once_with(0)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_list_paginated_offset_calculation(mock_task):
    mock_query = MagicMock()
    mock_query.count = AsyncMock(return_value=10)

    mock_query.offset.return_value.limit = AsyncMock(return_value=[])

    mock_task.all.return_value = mock_query

    await task_service.list_paginated(page=3, size=2)

    # offset = (3 - 1) * 2 = 4
    mock_query.offset.assert_called_once_with(4)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_complete_task_success(mock_task):
    fake_task = AsyncMock()
    fake_task.status = TaskStatus.PENDING
    fake_task.version = 1

    updated_task = AsyncMock()
    updated_task.status = TaskStatus.DONE

    mock_task.get = AsyncMock(side_effect=[fake_task, updated_task])
    mock_task.filter.return_value.update = AsyncMock(return_value=1)

    result = await task_service.complete_task(1)

    assert result.status == TaskStatus.DONE


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_complete_task_not_found(mock_task):
    mock_task.get = AsyncMock(return_value=None)

    with pytest.raises(NotFoundError):
        await task_service.complete_task(1)


@pytest.mark.asyncio
@patch("app.services.task_service.Task")
async def test_reopen_task_invalid_transition(mock_task):
    fake_task = AsyncMock()
    fake_task.status = TaskStatus.IN_PROGRESS
    fake_task.version = 1
    mock_task.filter.return_value.first = AsyncMock(return_value=fake_task)

    with pytest.raises(InvalidStatusTransitionError) as exc:
        await task_service.reopen_task(1)

    assert "Invalid status transition" in str(exc.value)


@pytest.mark.asyncio
async def test_complete_task_success_integration(task_factory):
    task = await task_factory(status=TaskStatus.PENDING)
    result = await task_service.complete_task(task.id)
    assert result.status == TaskStatus.DONE
