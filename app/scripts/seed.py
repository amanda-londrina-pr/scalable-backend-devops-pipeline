import structlog

from app.models.task_model import Task
from app.scripts.factories.task_factory import generate_task_data

logger = structlog.get_logger()


async def seed_tasks(quantity: int = 10):
    count = await Task.all().count()

    if count > 0:
        logger.info("seed_skipped_already_populated", count=count)
        return

    tasks = []

    for _ in range(quantity):
        data = generate_task_data()
        tasks.append(Task(**data))

    await Task.bulk_create(tasks)

    logger.info("seed_completed", total=quantity)
