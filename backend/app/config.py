"""Application configuration loaded from environment / backend/.env.

Keeps all runtime settings in one place. Integration credentials are
optional strings that are only provided through a real .env file, which is
git-ignored and must never be committed.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Resume Sync Platform"
    app_version: str = "0.1.0"
    environment: str = "development"

    # Local prototype uses SQLite. PostgreSQL can be introduced later by only
    # changing DATABASE_URL, e.g.:
    #   postgresql+psycopg://user:password@localhost:5432/resume_sync
    database_url: str = "sqlite+pysqlite:///./data/resume_sync.db"

    # Comma-separated list is supported via CORS_ORIGINS env var.
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # --- Integration settings (planned; no real credentials required yet) ---
    github_api_base_url: str = "https://api.github.com"
    github_token: str | None = None

    leetcode_api_base_url: str = "https://leetcode.com/api/graphql/"

    linkedin_api_base_url: str = "https://api.linkedin.com/v2"
    linkedin_client_id: str | None = None
    linkedin_client_secret: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
