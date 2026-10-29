# Resume Sync Platform

A collaborative web application that syncs developer activity (GitHub,
LeetCode, LinkedIn) into a curated profile and generates resumes from the
**user-approved** data only.

Two-person setup:

- **Backend** (Python 3 + FastAPI + SQLite): `backend/`
- **Frontend** (React + TypeScript + Vite): `frontend/`
- Collaboration rules: `docs/DEVELOPMENT.md`
- Endpoint contract: `docs/api-contract.md`

## Repository layout

```
resume-sync-platform/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # HTTP endpoints
│   │   ├── services/        # business logic
│   │   │   └── integrations/ # GitHub/LeetCode/LinkedIn clients (planned)
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── config.py        # settings from environment/.env
│   │   ├── database.py      # engine + sessions (SQLite now, PostgreSQL-ready)
│   │   └── main.py          # FastAPI app + CORS + routing
│   ├── tests/               # pytest suite
│   ├── requirements.txt
│   └── .env.example         # copy to .env locally, never commit .env
├── frontend/                # React + TS + Vite scaffold (dev proxy to :8000)
├── docs/                    # api-contract.md, DEVELOPMENT.md
└── README.md
```

## Quick start — backend

```powershell
cd backend
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env     # optional for the local prototype
.venv\Scripts\uvicorn app.main:app --reload --port 8000
.venv\Scripts\pytest          # run the tests
```

API docs at <http://localhost:8000/docs>.

## Quick start — frontend

```powershell
cd frontend
npm install
npm run dev     # http://localhost:5173, /api proxied to :8000
npm run build   # production build check
npm run lint
```

## Current status

Implemented now: `GET /api/health`, `GET/PUT /api/profile`,
`GET /api/sync/history`, `POST /api/resume/generate` (preview draft from
approved data), plus the frontend dashboard scaffold with a live health check.

Planned (intentionally answering `501`, nothing faked): the three sync
integrations
(`POST /api/sync/{github,leetcode,linkedin}`) and full resume document
rendering. Details: `docs/api-contract.md`.

## Safety rules

- Never commit `.env`, tokens, keys, databases or `node_modules` /
  `.venv` (see `.gitignore`).
- Integrations must only use official APIs and public data; LinkedIn syncing
  by scraping is prohibited.
- `main` stays runnable; work happens on `feature/backend-sync` and
  `feature/frontend-ui` via PRs (`docs/DEVELOPMENT.md`).
