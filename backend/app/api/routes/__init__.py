"""Route modules for the Resume Sync Platform API."""

from app.api.routes import health, profile, resume, sync  # noqa: F401

__all__ = ["health", "profile", "resume", "sync"]
