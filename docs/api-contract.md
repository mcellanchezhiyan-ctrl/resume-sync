# API Contract - Resume Sync Platform

Shared agreement between the backend (Python/FastAPI) and the frontend
(React/Vite). Both sides treat this file as the source of truth; changes to
any endpoint must be reflected here in the same PR.

- **Base URL (dev):** `http://localhost:8000` for direct calls, or relative `/api/...`
  through the Vite dev proxy (frontend dev server on `http://localhost:5173`).
- **Content type:** `application/json`
- **Auth:** none yet (single local user). A users/auth layer is planned.
- **Interactive docs:** FastAPI auto-generates `/docs` (Swagger UI) and `/redoc`.

## Endpoint status legend

- **Implemented** — working today, covered by backend tests.
- **Planned** — route exists in the contract only; the API intentionally
  answers `501 Not Implemented` until the feature is built. Nothing is
  fabricated in the meantime.

| Method | Path | Status |
| ------ | ---- | ------ |
| GET | `/api/health` | Implemented |
| GET | `/api/profile` | Implemented |
| PUT | `/api/profile` | Implemented |
| POST | `/api/sync/github` | Planned (501) |
| POST | `/api/sync/leetcode` | Planned (501) |
| POST | `/api/sync/linkedin` | Planned (501) |
| GET | `/api/sync/history` | Implemented |
| POST | `/api/resume/generate` | Implemented (preview) |

---

## GET /api/health — Implemented

Liveness and database connectivity check used by the frontend health widget.

**Response `200`**

```json
{
  "status": "ok",
  "app": "Resume Sync Platform",
  "version": "0.1.0",
  "environment": "development",
  "database": "connected",
  "time": "2026-10-29T04:31:22.866607Z"
}
```

`status` is `"degraded"` when the database is unreachable (`"database"`:
`"unavailable"`).

## GET /api/profile — Implemented

Returns the current user-approved profile. Creates an empty one on first call.

**Response `200`**

```json
{
  "id": 1,
  "full_name": null,
  "headline": null,
  "location": null,
  "email": null,
  "phone": null,
  "summary": null,
  "skills": [],
  "experiences": [],
  "education": [],
  "links": {},
  "updated_at": "2026-10-29T04:31:23.043020Z"
}
```

Entry shapes (`experiences[]`):

```json
{ "company": "Acme Corp", "role": "Software Engineer", "start": "2024-01", "end": null, "highlights": ["Built APIs"] }
```

Entry shapes (`education[]`):

```json
{ "institution": "Example University", "degree": "BSc CS", "start": "2019", "end": "2023" }
```

## PUT /api/profile — Implemented

Updates user-approved profile data. Semantics: partial update — only fields
present in the body are applied; unknown fields are rejected with `422` so
typos never silently disappear. **This is the only path into approved resume
data: sync results never modify the profile automatically.**

**Request body (any subset)**

```json
{
  "full_name": "Ada Lovelace",
  "headline": "Backend Engineer",
  "skills": ["Python", "FastAPI"],
  "experiences": [
    { "company": "Acme Corp", "role": "Software Engineer", "highlights": ["Built APIs"] }
  ]
}
```

**Response `200`** — full `Profile` shape as in `GET /api/profile`.

## POST /api/sync/github — Planned

Fetches PUBLIC profile/repository metadata through the official GitHub REST
API using a server-side token (`GITHUB_TOKEN` in `backend/.env`).

## POST /api/sync/leetcode — Planned

Fetches PUBLIC LeetCode statistics via the public GraphQL endpoint
(`LEETCODE_API_BASE_URL`). No credentials required for public data.

## POST /api/sync/linkedin — Planned

Official LinkedIn partner API via OAuth only. **Scraping or harvesting of
session cookies is prohibited in this project** (violates LinkedIn policy).

**Request body (all three, all fields optional)**

```json
{ "username": "octocat", "resume_url": "https://www.linkedin.com/in/you/", "dry_run": false }
```

**Current response until implemented — `501`**

```json
{
  "detail": {
    "source": "github",
    "status": "planned",
    "message": "github sync is planned, not implemented yet. Credentials: missing.",
    "records_fetched": 0,
    "started_at": "2026-10-29T04:31:23.146668Z",
    "finished_at": "2026-10-29T04:31:23.146714Z"
  }
}
```

**Intended response once real — `200`** — `SyncResult` (same shape, with
`status`: `"ok"` / `"error"` / `"skipped"`).

When implemented, syncs will:
1. fetch raw provider data using server-side credentials only (never from the
   request body),
2. store the raw payload in `ExternalProfileSnapshot`,
3. let the user review and approve individual changes into their profile
   (`PUT /api/profile`). Nothing reaches approved resume data automatically.

## GET /api/sync/history — Implemented

Lists past sync runs, newest first. Empty until syncs are implemented.

**Query params:** `limit` (int, default 50, max 500)

**Response `200`**

```json
[
  {
    "id": 1,
    "source": "github",
    "status": "error",
    "message": "GITHUB_TOKEN is not set.",
    "records_fetched": 0,
    "started_at": "2026-10-29T04:31:23.146668Z",
    "finished_at": "2026-10-29T04:31:23.146714Z"
  }
]
```

## POST /api/resume/generate — Implemented (preview)

Generates a structured resume **draft** strictly from user-approved profile
data. Full document/PDF rendering is a future feature; this returns the
structured draft that the resume builder UI will consume.

**Request body (optional)**

```json
{ "title": "Backend CV", "sections": ["summary", "skills", "experience", "education"] }
```

- `title`: non-blank, max 120 chars (default `"Generated Resume"`).
- `sections`: subset of `summary | skills | experience | education`
  (default: all four).
- Empty/no body uses the defaults.

**Response `200`**

```json
{
  "title": "Backend CV",
  "generated_at": "2026-10-29T04:31:43.835512Z",
  "based_on_profile_id": 1,
  "summary": "Backend engineer.",
  "skills": ["Python"],
  "experiences": [],
  "education": [],
  "notes": [
    "Preview generator: only user-approved profile data is included."
  ]
}
```

**Errors**

- `400` if the body requests `include_external_synced_data: true` — external
  sync data must be reviewed and approved via `PUT /api/profile` first.
- `422` for malformed bodies (e.g. blank title).

---

## Conventions for both sides

- Timestamps are ISO-8601 UTC strings.
- Field names are `snake_case` on both sides.
- Error responses use FastAPI's `{"detail": ...}` shape.
- Adding an endpoint? Update this file and `backend/tests` in the same PR.
