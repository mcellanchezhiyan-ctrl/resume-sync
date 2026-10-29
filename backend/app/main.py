"""FastAPI application entry point.

Run from backend/ with:
    uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, profile, resume, sync
from app.config import get_settings
from app.database import create_db_and_tables

DESCRIPTION = """
Resume Sync Platform backend API.

Syncs developer activity from GitHub, LeetCode and LinkedIn into a curated
profile, then generates resumes from the user-approved data.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=DESCRIPTION,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(profile.router)
    app.include_router(sync.router)
    app.include_router(resume.router)
    return app


app = create_app()
