from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: SecretStr
    redis_url: SecretStr

    # Object storage config
    minio_root_user: str
    minio_root_password: SecretStr

    # #s3 compatible storage 
    # s3_endpoint_url: str 
    # s3_access_key: str 
    # s3_secret_key: SecretStr 
    # s3_bucket: str

    #LLM config 
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_api_key: SecretStr | None = None  # set none until we decide to use llm
    llm_model: str | None = None

    # Logging config
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    log_format: Literal["console", "json"] = "console"


@lru_cache
def get_settings() -> Settings:
    return Settings()
