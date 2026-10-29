"""Resume generation schemas."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.profile import EducationEntry, ExperienceEntry


class ResumeGenerateRequest(BaseModel):
    title: str = Field(default="Generated Resume", min_length=1, max_length=120)
    sections: list[str] = Field(
        default_factory=lambda: ["summary", "skills", "experience", "education"]
    )
    # Always false in the request: external sync data only enters a resume
    # after being reviewed and approved into the profile via PUT /api/profile.
    include_external_synced_data: bool = False

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value


class ResumeDraft(BaseModel):
    title: str
    generated_at: datetime
    based_on_profile_id: int
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    experiences: list[ExperienceEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
