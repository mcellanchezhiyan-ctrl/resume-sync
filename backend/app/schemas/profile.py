"""Profile request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExperienceEntry(BaseModel):
    company: str
    role: str
    start: str | None = None
    end: str | None = None
    highlights: list[str] = Field(default_factory=list)


class EducationEntry(BaseModel):
    institution: str
    degree: str | None = None
    start: str | None = None
    end: str | None = None


class ProfileResponse(BaseModel):
    """Approved profile data as stored and returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str | None = None
    headline: str | None = None
    location: str | None = None
    email: str | None = None
    phone: str | None = None
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    experiences: list[ExperienceEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    links: dict[str, str] = Field(default_factory=dict)
    updated_at: datetime


class ProfileUpdate(BaseModel):
    """Partial update of user-approved profile data.

    Only fields present in the request body are applied; missing fields keep
    their current values. Unknown fields are rejected so typos never silently
    disappear. This is the ONLY path into approved resume data - sync results
    never write here.
    """

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = None
    headline: str | None = None
    location: str | None = None
    email: str | None = None
    phone: str | None = None
    summary: str | None = None
    skills: list[str] | None = None
    experiences: list[ExperienceEntry] | None = None
    education: list[EducationEntry] | None = None
    links: dict[str, str] | None = None
