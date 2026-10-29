"""Database engine and session management.

The same code runs on SQLite (local prototype) and PostgreSQL (future) because
only the DATABASE_URL changes. No SQLite-only features are used; JSON columns
map to SQLite TEXT-JSON and PostgreSQL JSON via SQLAlchemy's JSON type.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def create_db_engine(settings=None):
    """Build an engine from settings. Overridable for tests."""
    settings = settings or get_settings()
    url = settings.database_url
    kwargs: dict = {"future": True}
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **kwargs)


engine = create_db_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables() -> None:
    """Create all tables. Called on app startup (lifespan)."""
    from app import models  # noqa: F401  (import registers the models)

    Base.metadata.create_all(bind=engine)
