"""Profile service: read/upsert user-approved profile data."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Profile
from app.schemas.profile import ProfileUpdate

SINGLE_USER_PROFILE_ID = 1


def get_or_create_profile(db: Session) -> Profile:
    """Return the local profile row, creating an empty one if needed.

    The prototype is single-user; a users table will be introduced alongside
    PostgreSQL and authentication.
    """
    profile = db.scalar(select(Profile).order_by(Profile.id).limit(1))
    if profile is None:
        profile = Profile()
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def update_profile(db: Session, payload: ProfileUpdate) -> Profile:
    """Apply only the fields present in the payload (approved data only)."""
    profile = get_or_create_profile(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
