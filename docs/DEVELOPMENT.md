# Development Guide - Resume Sync Platform

Two-developer collaboration setup:

- **Backend (you):** Python/FastAPI - APIs, integrations, database, profile
  synchronization. Branch: `feature/backend-sync`.
- **Frontend (your friend):** React/TypeScript/Vite. Branch:
  `feature/frontend-ui`.
- **Stable integration branch:** `main` - always runnable, pushed only via
  reviewed PRs.

Prerequisites: Python 3.12+ (project developed on 3.14), Node.js 20+ with npm,
Git 2.30+.

---

## Backend setup (Windows PowerShell)

```powershell
cd backend
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env      # optional for the prototype; edit values locally
```

Run the API (from `backend/`, with the venv active or via full path):

```powershell
.venv\Scripts\uvicorn app.main:app --reload --port 8000
```

Interactive API docs: <http://localhost:8000/docs>

Run the tests (from `backend/`):

```powershell
.venv\Scripts\pytest
```

macOS/Linux equivalents: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`,
`.venv/bin/uvicorn ...`, `.venv/bin/pytest`.

## Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

- Dev server: <http://localhost:5173> (default port configured in vite.config.ts).
- `/api/*` requests are proxied to `http://localhost:8000` during development.
- Production check: `npm run build` (runs `tsc -b && vite build`), lint: `npm run lint`.

Verify the full stack: start the backend first, then `npm run dev`; the health
widget in the header should read "API healthy".

---

## Git workflow

### Branch model

- `main` — stable integration branch. Protected by habit: change through PRs.
- `feature/backend-sync` — your backend work (exists already).
- `feature/frontend-ui` — your friend's frontend work (already branched from
  the same scaffold commit).

### Branch naming convention

`<type>/<area>-<short-topic>`, types: `feature`, `bugfix`, `docs`, `chore`.

Examples: `feature/backend-linkedin-sync`, `feature/frontend-profile-form`,
`bugfix/backend-sync-history-limit`, `docs/api-contract-resume`.

### Daily loop (applies to both developers)

1. **Start of the day** — update main and your branch:
   ```powershell
   git switch main
   git pull origin main
   git switch feature/frontend-ui
   git pull origin feature/frontend-ui
   git rebase origin main   # feature branches are single-owner, rebasing is safe
   ```
2. **Work in small commits** — imperative messages, e.g.
   `Add resume draft section filtering`.
3. **Before pushing** — run your own verification: backend `pytest`, frontend
   `npm run build && npm run lint`. Do not push red code.
4. **Push & open a PR into main**:
   ```powershell
   git push -u origin feature/frontend-ui
   gh pr create --base main --head feature/frontend-ui
   ```
   or create the PR in the GitHub web UI.
5. **Review** — the other person reviews every PR before merge (she reviews
   backend contract changes that touch `frontend/src/lib/api.ts`, you review
   anything that changes endpoint responses).
6. **Merge** into `main`; delete the branch only when its feature is fully
   delivered.

### Conflict rules (avoid overwriting each other)

- Frontend and backend live in separate top-level folders (`frontend/`,
  `backend/`) - stay in your folder and conflicts are rare.
- **Shared files that require care:** `docs/api-contract.md`,
  `frontend/src/lib/api.ts`, `README.md`, `backend/requirements.txt`,
  `frontend/package.json`. Any change touching these must be announced in the
  PR description; this also applies to `docs/api-contract.md` edits.
- Merge contract/API changes into your feature branch early (`git rebase
  origin main`) rather than force-fixing later.
- **Never** `git push --force`/`--force-with-lease` on shared branches, never
  commit `node_modules/`, `.venv/`, databases, `.env` or credentials
  (`git status` first if unsure).

### Secrets policy

- Real credentials live only in `backend/.env` (git-ignored) and never in the
  repository, logs, screenshots or PR descriptions.
- Third-party data fetched by integrations goes to
  `ExternalProfileSnapshot`, separate from the user-approved `Profile`.
- LinkedIn data may only come from the official partner API via OAuth - no
  scraping, no session-cookie harvesting.

---

## Roadmap (who owns what)

Short term:

- Backend: GitHub public-data sync (token via `.env`), LeetCode public stats
  sync, generic sync-history recording, then decide on resume renderer.
- Frontend: profile editor, sync triggers + history view, resume draft viewer.
- Joint: first PostgreSQL migration decision (change `DATABASE_URL` only),
  users/auth design before any multi-user deployment.
