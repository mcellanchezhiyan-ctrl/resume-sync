"""Sync service.

Runs third-party integrations and records their history. The actual
integrations are intentionally NOT implemented yet: run_sync raises
SyncNotImplementedError until the integration clients are wired up on
feature/backend-sync. Nothing fake is ever produced.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SyncHistory
from app.schemas.sync import SyncRequestBody, SyncResult
from app.services.integrations import get_client


class SyncNotImplementedError(RuntimeError):
    """Raised when an integration is planned but not wired up yet."""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _record(
    db: Session,
    source: str,
    status: str,
    message: str | None,
    records_fetched: int,
    started_at: datetime,
    finished_at: datetime | None,
) -> SyncHistory:
    entry = SyncHistory(
        source=source,
        status=status,
        message=message,
        records_fetched=records_fetched,
        started_at=started_at,
        finished_at=finished_at,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def run_sync(db: Session, source: str, request: SyncRequestBody | None) -> SyncResult:
    """Trigger a sync for `source`. Currently raises SyncNotImplementedError.

    Implementation plan (do not fabricate data in the meantime):
      1. instantiate the source client from app.services.integrations,
      2. fetch public data using server-side credentials from settings,
      3. store raw output in ExternalProfileSnapshot,
      4. propose changes to the user, who approves them into the Profile.
    """
    started_at = utcnow()
    client = get_client(source)
    credentials = "configured" if client.has_credentials() else "missing"
    message = (
        f"{client.provider_name} sync is planned, not implemented yet. "
        f"Client module: app.services.integrations.{source}_client. "
        f"Credentials: {credentials}."
    )
    raise SyncNotImplementedError(message)


def record_error(
    db: Session, source: str, exc: Exception, started_at: datetime
) -> SyncHistory:
    return _record(
        db,
        source,
        status="error",
        message=str(exc),
        records_fetched=0,
        started_at=started_at,
        finished_at=utcnow(),
    )


def list_history(db: Session, limit: int = 50) -> list[SyncHistory]:
    return list(db.scalars(select(SyncHistory).order_by(SyncHistory.id.desc()).limit(limit)))
