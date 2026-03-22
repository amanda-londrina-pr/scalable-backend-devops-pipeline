# app/scripts/run_seed.py

import structlog
from tortoise import Tortoise

from app.core.settings import get_settings
from app.scripts.seed import seed_tasks

logger = structlog.get_logger()


async def run():
    settings = get_settings()
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()

    try:
        await seed_tasks()
    except Exception:
        logger.exception("seed_tasks_error", exc_info=True)
        raise

    await Tortoise.close_connections()
