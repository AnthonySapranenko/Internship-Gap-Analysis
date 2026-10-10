"""Application settings, read from environment variables or a .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="GAP_", extra="ignore")

    # Origins allowed to call the API from a browser (the Vite dev server by default).
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
