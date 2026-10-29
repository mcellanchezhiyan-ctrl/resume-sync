# Resume Sync Platform - frontend

React + TypeScript + Vite scaffold for the Resume Sync Platform.

- Dev server proxies `/api` calls to the FastAPI backend at `http://localhost:8000` (see `vite.config.ts`).
- Reusable API client: `src/lib/api.ts`.
- Health-check component calling `GET /api/health`: `src/components/HealthCheck.tsx`.

The full resume-builder UI lives on the `feature/frontend-ui` branch.
See `../docs/DEVELOPMENT.md` for setup, workflow and branch conventions.
