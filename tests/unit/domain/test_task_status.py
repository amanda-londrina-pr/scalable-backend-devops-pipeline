# tests/unit/domain/test_task_status.py

import pytest

from app.domain.enums.task_status import TaskStatus
from app.domain.errors import InvalidStatusTransitionError
from app.domain.services.task_status_service import ALLOWED_TRANSITIONS
from app.domain.services.task_status_service import validate_status_transition


# =========================
# ✅ VALID TRANSITIONS
# =========================

@pytest.mark.parametrize(
    "current,new",
    [
        (TaskStatus.PENDING, TaskStatus.IN_PROGRESS),
        (TaskStatus.PENDING, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    ],
)
def test_valid_transitions(current, new):
    # Should NOT raise exception
    validate_status_transition(current, new)


@pytest.mark.parametrize(
    "current,new",
    [
        (TaskStatus.PENDING, TaskStatus.PENDING),
        (TaskStatus.IN_PROGRESS, TaskStatus.PENDING),
        (TaskStatus.DONE, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.PENDING),
    ],
)
def test_invalid_transitions(current, new):
    with pytest.raises(InvalidStatusTransitionError):
        validate_status_transition(current, new)


def test_invalid_type_raises_error():
    with pytest.raises(TypeError):
        validate_status_transition("pending", "done")


def test_enum_values_are_strings():
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.IN_PROGRESS.value == "in_progress"
    assert TaskStatus.DONE.value == "done"


def test_all_status_have_defined_transitions():
    for status in TaskStatus:
        assert status in ALLOWED_TRANSITIONS


def test_no_unexpected_transition_allowed():
    all_status = set(TaskStatus)

    for current, allowed_list in ALLOWED_TRANSITIONS.items():
        for new in all_status:
            if new in allowed_list:
                continue

            with pytest.raises(InvalidStatusTransitionError):
                validate_status_transition(current, new)


@pytest.mark.parametrize("invalid", ["pending", 123, None])
def test_invalid_current_type(invalid):
    with pytest.raises(TypeError):
        validate_status_transition(invalid, TaskStatus.DONE)
