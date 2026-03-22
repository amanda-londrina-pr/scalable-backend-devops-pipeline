import pytest

from app.domain.enums.task_status import TaskStatus
from app.services import task_service


@pytest.mark.asyncio
async def test_complete_task_success_integration(task_factory):
    task = await task_factory(status=TaskStatus.PENDING)
    result = await task_service.complete_task(task.id)
    assert result.status == TaskStatus.DONE
