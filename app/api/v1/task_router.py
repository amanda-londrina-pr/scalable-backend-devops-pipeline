# app.api.v1.task_router.py
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
def list_tasks():
    return []
