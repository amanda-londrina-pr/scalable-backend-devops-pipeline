# app.api.routes.task_routes.py
from fastapi import APIRouter

router = APIRouter()

tasks = []

@router.get("/tasks")
def get_tasks():
    return tasks

@router.post("/tasks")
def create_task(task: dict):
    tasks.append(task)
    return task

