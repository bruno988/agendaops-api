from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AgendaOps API"
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://agendaops:agendaops@localhost:5432/agendaops"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
