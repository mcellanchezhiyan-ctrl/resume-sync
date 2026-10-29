"""Resume draft generation endpoint (preview, approved data only)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.resume import ResumeDraft, ResumeGenerateRequest
from app.services import profile_service, resume_service

router = APIRouter(prefix="/api", tags=["resume"])


@router.post("/resume/generate", response_model=ResumeDraft)
def generate_resume(
    request: ResumeGenerateRequest, db: Session = Depends(get_db)
) -> ResumeDraft:
    """Generate a preview resume draft from APPROVED profile data only.

    Full resume document/PDF generation is a future feature; this endpoint
    returns the structured draft the resume builder will consume.
    """
    if request.include_external_synced_data:
        raise HTTPException(
            status_code=400,
            detail=(
                "External sync data cannot be used directly. Review it and "
                "approve it into your profile via PUT /api/profile first."
            ),
        )
    profile = profile_service.get_or_create_profile(db)
    return resume_service.build_draft(profile, request)
