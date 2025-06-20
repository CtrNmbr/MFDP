import pathlib
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    JWT_SECRET_KEY: Optional[str] = None

    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None

    RABBITMQ_USER: Optional[str] = None
    RABBITMQ_PASSWORD: Optional[str] = None
    RABBITMQ_HOST: Optional[str] = None
    RABBITMQ_PORT: Optional[int] = None

    model_config = SettingsConfigDict(
        env_file=str(pathlib.Path(__file__).parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra='ignore'# Extra inputs are not permitted [type=extra_forbidden, input_value='postgres', input_type=str] # pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings worker-1       | db_password
    )

@lru_cache()
def import_settings() -> Settings:
    return Settings()