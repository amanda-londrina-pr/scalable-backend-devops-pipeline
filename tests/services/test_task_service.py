from unittest.mock import AsyncMock, patch

import pytest

from app.domain.errors import NotFoundError
from app.services import task_service


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
