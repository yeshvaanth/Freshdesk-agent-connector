from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    freshdesk_domain: str | None = None
    freshdesk_api_key: str | None = None

    app_mode: Literal["mock", "freshdesk"] = "mock"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()