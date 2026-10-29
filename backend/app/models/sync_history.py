"""Sync bookkeeping and raw third-party payload storage.

SyncHistory documents every integration run (even future failures).
ExternalProfileSnapshot keeps raw provider output completely separate from the
approved Profile so nothing reaches a resume without explicit user approval.
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SyncHistory(Base):
    __tablename__ = "sync_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(50))  # github | leetcode | linkedin
    status: Mapped[str] = mapped_column(String(32))  # ok | error | skipped | ...
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    records_fetched: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ExternalProfileSnapshot(Base):
    __tablename__ = "external_profile_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(50))
    external_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
