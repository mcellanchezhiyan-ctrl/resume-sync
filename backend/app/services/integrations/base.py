"""Shared plumbing for planned integration clients."""

from app.config import Settings, get_settings


class IntegrationError(Exception):
    """Base error for integration problems."""


class IntegrationNotConfiguredError(IntegrationError):
    """Server-side credentials are missing, so the sync cannot run."""


class BaseIntegrationClient:
    """Minimal shared behaviour; fetch() is intentionally unimplemented."""

    provider_name: str = "base"

    def __init__(self, settings: Settings | None = None):
        self.settings = get_settings() if settings is None else settings

    def has_credentials(self) -> bool:
        """Whether the provider is configured in the environment."""
        return False

    def fetch(self, subject: str) -> dict:
        """Fetch public data for `subject`.

        Returns a raw dict for ExternalProfileSnapshot. Never raises fake
        data: implementations raise NotImplementedError/IntegrationError.
        """
        raise NotImplementedError(
            f"{self.provider_name} integration is planned, not implemented."
        )
