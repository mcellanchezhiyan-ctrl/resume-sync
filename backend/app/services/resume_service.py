"""Resume draft generation.

Builds a preview resume draft strictly from user-approved profile data.
External/synced data is never used here unless it was approved into the
profile via PUT /api/profile.
"""

from datetime import datetime, timezone

from pydantic import ValidationError

from app.models import Profile
from app.schemas.profile import EducationEntry, ExperienceEntry
from app.schemas.resume import ResumeDraft, ResumeGenerateRequest


def build_draft(profile: Profile, request: ResumeGenerateRequest) -> ResumeDraft:
    sections = [s.strip().lower() for s in request.sections]
    notes: list[str] = [
        "Preview generator: only user-approved profile data is included.",
        "Third-party sync data must be reviewed and approved via PUT /api/profile "
        "to appear in a resume.",
    ]
    if not profile.full_name:
        notes.append("Profile is empty; PUT /api/profile to add approved data.")

    experiences: list[ExperienceEntry] = []
    education: list[EducationEntry] = []
    if "experience" in sections:
        raw = profile.experiences or []
        for item in raw:
            try:
                experiences.append(ExperienceEntry.model_validate(item))
            except ValidationError:
                continue
    if "education" in sections:
        raw = profile.education or []
        for item in raw:
            try:
                education.append(EducationEntry.model_validate(item))
            except ValidationError:
                continue

    return ResumeDraft(
        title=request.title,
        generated_at=datetime.now(timezone.utc),
        based_on_profile_id=profile.id,
        summary=profile.summary if "summary" in sections else None,
        skills=profile.skills or [] if "skills" in sections else [],
        experiences=experiences,
        education=education,
        notes=notes,
    )
