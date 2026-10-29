"""API tests for profile, sync and resume endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_get_profile_creates_default(client: TestClient):
    response = client.get("/api/profile")
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] is None
    assert body["skills"] == []
    assert body["experiences"] == []
    assert body["education"] == []


def test_put_profile_updates_and_persists(client: TestClient):
    response = client.put(
        "/api/profile",
        json={
            "full_name": "Ada Lovelace",
            "headline": "Backend Engineer",
            "skills": ["Python", "FastAPI"],
            "experiences": [
                {
                    "company": "Acme Corp",
                    "role": "Software Engineer",
                    "start": "2024-01",
                    "highlights": ["Built APIs"],
                }
            ],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] == "Ada Lovelace"
    assert body["skills"] == ["Python", "FastAPI"]
    assert body["experiences"][0]["company"] == "Acme Corp"

    updated = client.get("/api/profile").json()
    assert updated["full_name"] == "Ada Lovelace"


def test_put_profile_partial_update_keeps_other_fields(client: TestClient):
    client.put("/api/profile", json={"full_name": "Ada Lovelace", "skills": ["Python"]})
    response = client.put("/api/profile", json={"headline": "Backend Engineer"})
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] == "Ada Lovelace"
    assert body["headline"] == "Backend Engineer"
    assert body["skills"] == ["Python"]


@pytest.mark.parametrize("source", ["github", "leetcode", "linkedin"])
def test_sync_sources_are_planned_not_implemented(source: str, client: TestClient):
    response = client.post(f"/api/sync/{source}", json={})
    assert response.status_code == 501
    detail = response.json()["detail"]
    assert detail["source"] == source
    assert detail["status"] == "planned"


def test_sync_unknown_source_rejected(client: TestClient):
    response = client.post("/api/sync/instagram", json={})
    assert response.status_code == 422


def test_sync_history_empty_initially(client: TestClient):
    response = client.get("/api/sync/history")
    assert response.status_code == 200
    assert response.json() == []


def test_resume_generate_returns_approved_only_draft(client: TestClient):
    client.put(
        "/api/profile",
        json={
            "full_name": "Ada Lovelace",
            "summary": "Backend engineer.",
            "skills": ["Python"],
            "experiences": [
                {"company": "Acme Corp", "role": "Software Engineer"}
            ],
            "education": [{"institution": "Uni", "degree": "BSc"}],
        },
    )
    response = client.post(
        "/api/resume/generate", json={"title": "My CV", "sections": ["summary", "skills"]}
    )
    assert response.status_code == 200
    draft = response.json()
    assert draft["title"] == "My CV"
    assert draft["summary"] == "Backend engineer."
    assert draft["skills"] == ["Python"]
    assert draft["experiences"] == []  # filtered out by requested sections
    assert "only user-approved profile data" in draft["notes"][0]


def test_resume_generate_rejects_external_sync_data_request(client: TestClient):
    response = client.post(
        "/api/resume/generate", json={"include_external_synced_data": True}
    )
    assert response.status_code == 400
