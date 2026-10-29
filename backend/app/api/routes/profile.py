"""Profile endpoints (user-approved resume data only)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services import profile_service

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/profile", response_model=ProfileResponse)
def read_profile(db: Session = Depends(get_db)) -> ProfileResponse:
    """Return the current approved profile (creating an empty one if needed)."""
    return profile_service.get_or_create_profile(db)


@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdate, db: Session = Depends(get_db)
) -> ProfileResponse:
    """Update approved profile fields (partial body is applied field-by-field)."""
    return profile_service.update_profile(db, payload)
