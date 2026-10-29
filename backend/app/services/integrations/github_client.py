"""Planned GitHub integration.

Plan: use the official GitHub REST API (https://docs.github.com/en/rest) with
a server-side fine-grained token for PUBLIC profile and repository metadata
only. Requires GITHUB_TOKEN in backend/.env. No scraping.
"""

from app.services.integrations.base import (
    BaseIntegrationClient,
    IntegrationNotConfiguredError,
)


class GitHubClient(BaseIntegrationClient):
    provider_name = "github"

    def has_credentials(self) -> bool:
        return bool(self.settings.github_token)

    def fetch(self, username: str) -> dict:
        if not self.has_credentials():
            raise IntegrationNotConfiguredError(
                "GITHUB_TOKEN is not set. Add it to backend/.env before enabling "
                "GitHub sync."
            )
        raise NotImplementedError(
            "GitHub sync is planned. TODO on feature/backend-sync: "
            f"GET {self.settings.github_api_base_url}/users/{username} and "
            "…/repos with the Authorization header; normalise into an "
            "ExternalProfileSnapshot."
        )
