"""Schema validation tests for core request/response models."""

import pytest
from pydantic import ValidationError

from app.schemas.profile import EducationEntry, ExperienceEntry, ProfileUpdate
from app.schemas.resume import ResumeGenerateRequest
from app.schemas.sync import SyncRequestBody, SyncResult
from datetime import datetime, timezone


def test_experience_entry_valid():
    entry = ExperienceEntry(company="Acme", role="Engineer", highlights=["did things"])
    assert entry.highlights == ["did things"]


def test_experience_entry_requires_company_and_role():
    with pytest.raises(ValidationError):
        ExperienceEntry(role="Engineer")
    with pytest.raises(ValidationError):
        ExperienceEntry()


def test_education_entry_valid():
    entry = EducationEntry(institution="Uni", degree="BSc", start="2019", end="2023")
    assert entry.institution == "Uni"


def test_profile_update_partial_fields_default_none():
    payload = ProfileUpdate(full_name="Ada Lovelace")
    dumped = payload.model_dump(exclude_unset=True)
    assert dumped == {"full_name": "Ada Lovelace"}


def test_profile_update_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        ProfileUpdate(full_name="Ada", evil_field="boom")


def test_sync_result_status_validation():
    result = SyncResult(
        source="github",
        status="planned",
        message="not implemented",
        started_at=datetime.now(timezone.utc),
    )
    assert result.records_fetched == 0
    with pytest.raises(ValidationError):
        SyncResult(
            source="github",
            status="surprise",  # invalid status
            message="bad",
            started_at=datetime.now(timezone.utc),
        )


def test_sync_request_rejects_invalid_url():
    with pytest.raises(ValidationError):
        SyncRequestBody(resume_url="not a url")
    body = SyncRequestBody(username="octocat", dry_run=True)
    assert body.dry_run is True


def test_resume_generate_defaults():
    request = ResumeGenerateRequest()
    assert "summary" in request.sections
    assert request.include_external_synced_data is False


def test_resume_generate_rejects_empty_title():
    with pytest.raises(ValidationError):
        ResumeGenerateRequest(title="   ")
