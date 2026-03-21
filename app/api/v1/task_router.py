# app.api.v1.task_router.py
from fastapi import APIRouter, HTTPException
from fastapi import Query
from fastapi import Response, status

from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskSchema, PaginatedTaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=PaginatedTaskResponse)
async def list_all(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100)
):
    task_page = await task_service.list_all(page, size)

    return {
        "data": await TaskSchema.from_queryset(task_page.data),
        "meta": {
            "total": task_page.total,
            "page": task_page.page,
            "page_size": task_page.page_size,
            "total_pages": task_page.total_pages,
        }
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def create(data: TaskCreate):
    task = await task_service.create(data)
    return await TaskSchema.from_tortoise_orm(task)


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int):
    task = await task_service.get_by_id(task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    return await TaskSchema.from_tortoise_orm(task)


@router.put("/{task_id}", response_model=TaskSchema)
async def update(task_id: int, data: TaskUpdate):
    task = await task_service.update(task_id, data.model_dump(exclude_unset=True))

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    return await TaskSchema.from_tortoise_orm(task)


@router.delete("/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: int):
    success = await task_service.delete_by_id(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    # return {"message": "Task deleted successfully."}
    return Response(status_code=status.HTTP_204_NO_CONTENT)
