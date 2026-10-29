"""Sync (third-party integration) schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

SyncSource = Literal["github", "leetcode", "linkedin"]

SYNC_SOURCES: tuple[str, ...] = ("github", "leetcode", "linkedin")


class SyncRequestBody(BaseModel):
    """Optional parameters for a sync trigger.

    Credentials never come through the request body - they live only in
    backend/.env on the server.
    """

    # GitHub / LeetCode handle to sync (optional for the single local profile).
    username: str | None = None
    # LinkedIn: a URL the user owns; used by the blocked-but-scoped LinkedIn
    # import flow, never by scraping.
    resume_url: HttpUrl | None = None
    # When true the integration is asked to fetch and store a snapshot without
    # proposing any changes to approved profile data.
    dry_run: bool = False


class SyncResult(BaseModel):
    source: SyncSource
    status: Literal["planned", "ok", "error", "skipped"]
    message: str
    records_fetched: int = 0
    started_at: datetime
    finished_at: datetime | None = None


class SyncHistoryEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    status: str
    message: str | None = None
    records_fetched: int = 0
    started_at: datetime
    finished_at: datetime | None = None
