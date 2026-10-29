"""Integration client package.

Each planned provider has a stub client that documents exactly what the real
integration will do. `fetch` implementations are TODO: no fabricated data,
no scraping of restricted sources (notably LinkedIn).
"""

from app.services.integrations.base import (
    BaseIntegrationClient,
    IntegrationError,
    IntegrationNotConfiguredError,
)
from app.services.integrations.github_client import GitHubClient
from app.services.integrations.leetcode_client import LeetCodeClient
from app.services.integrations.linkedin_client import LinkedInClient

_CLIENTS: dict[str, type[BaseIntegrationClient]] = {
    "github": GitHubClient,
    "leetcode": LeetCodeClient,
    "linkedin": LinkedInClient,
}


def get_client(source: str) -> BaseIntegrationClient:
    client_cls = _CLIENTS.get(source)
    if client_cls is None:
        raise IntegrationError(f"Unknown integration source: {source}")
    return client_cls()


__all__ = [
    "BaseIntegrationClient",
    "IntegrationError",
    "IntegrationNotConfiguredError",
    "GitHubClient",
    "LeetCodeClient",
    "LinkedInClient",
    "get_client",
]
