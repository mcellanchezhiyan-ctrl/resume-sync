"""Sync trigger and history endpoints.

The three sync sources (github, leetcode, linkedin) are PLANNED features:
this module never invents their results. A trigger currently answers with
HTTP 501 and a SyncResult payload with status="planned".
"""

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sync import (
    SYNC_SOURCES,
    SyncHistoryEntry,
    SyncRequestBody,
    SyncResult,
)
from app.services import sync_service

router = APIRouter(prefix="/api", tags=["sync"])


@router.post(
    "/sync/{source}",
    response_model=SyncResult,
    responses={
        501: {
            "description": "Integration is planned but not implemented yet",
            "content": {
                "application/json": {
                    "example": {
                        "source": "github",
                        "status": "planned",
                        "message": "github sync is planned, not implemented yet.",
                        "records_fetched": 0,
                    }
                }
            },
        }
    },
)
def trigger_sync(
    source: Literal["github", "leetcode", "linkedin"] = Path(
        ..., description="Sync source to trigger"
    ),
    request: SyncRequestBody | None = None,
    db: Session = Depends(get_db),
) -> SyncResult:
    started_at = sync_service.utcnow()
    source_str = source if source in SYNC_SOURCES else str(source)
    try:
        return sync_service.run_sync(db, source_str, request)
    except sync_service.SyncNotImplementedError as exc:
        result = SyncResult(
            source=source_str,
            status="planned",
            message=str(exc),
            records_fetched=0,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )
        raise HTTPException(status_code=501, detail=result.model_dump(mode="json")) from exc
    except Exception as exc:  # real integration failures get recorded
        sync_service.record_error(db, source_str, exc, started_at)
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/sync/history", response_model=list[SyncHistoryEntry])
def read_sync_history(
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[SyncHistoryEntry]:
    """List past sync runs (newest first)."""
    return sync_service.list_history(db, limit=limit)
