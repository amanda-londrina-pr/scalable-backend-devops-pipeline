# app.core.settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Scalable Backend Devops Pipeline"
    DEBUG: bool = True
    ENV: str = "development"
    DATABASE_URL: str = "sqlite://:memory:"

    # class Config:
    #     env_file = ".env"


settings = Settings()
