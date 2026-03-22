# app.core.settings.py

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment


class Settings(BaseSettings):
    # não usamos .env e ignoramos extra variables.
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    # APP
    PROJECT_NAME: str = "Scalable Backend Devops Pipeline"
    DEBUG: bool = True
    ENV: Environment = Environment.DEVELOPMENT

    # SEED
    SEED_ON_START: bool = True

    # DB
    DATABASE_URL: str = "sqlite://:memory:"

    # ORM
    APP_MODELS: List[str] = ["app.models.task_model"]

    @property
    def TORTOISE_ORM(self) -> dict:
        return {
            "connections": {"default": self.DATABASE_URL},
            "apps": {
                "models": {
                    "models": self.APP_MODELS,
                    "default_connection": "default",
                }
            },
        }

    # HELPERS
    @property
    def is_dev(self) -> bool:
        return self.ENV == Environment.DEVELOPMENT

    @property
    def is_test(self) -> bool:
        return self.ENV == Environment.TEST

    @property
    def is_prod(self) -> bool:
        return self.ENV == Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    return Settings()


class TestSettings(Settings):
    ENV: Environment = Environment.TEST
    DATABASE_URL: str = "sqlite://:memory:"
    SEED_ON_START: bool = False
