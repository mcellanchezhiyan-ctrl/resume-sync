"""Planned LinkedIn integration - IMPORTANT POLICY CONSTRAINTS.

LinkedIn's Official partner API (OAuth 2.0, client credentials) is the only
acceptable data source. Scraping or harvesting session cookies violates
LinkedIn's Terms of Service and is explicitly forbidden in this project.
Until LINKEDIN_CLIENT_ID/LINKEDIN_CLIENT_SECRET (backend/.env) exist and the
OAuth flow is implemented, this integration stays planned.
"""

from app.services.integrations.base import (
    BaseIntegrationClient,
    IntegrationNotConfiguredError,
)


class LinkedInClient(BaseIntegrationClient):
    provider_name = "linkedin"

    def has_credentials(self) -> bool:
        return bool(
            self.settings.linkedin_client_id and self.settings.linkedin_client_secret
        )

    def fetch(self, subject: str) -> dict:
        if not self.has_credentials():
            raise IntegrationNotConfiguredError(
                "LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET are not set. "
                "LinkedIn sync stays planned until the official OAuth flow is "
                "implemented. Scraping is not allowed in this project."
            )
        raise NotImplementedError(
            "LinkedIn sync is planned. TODO on feature/backend-sync: OAuth 2.0 "
            "client-credentials flow against "
            f"{self.settings.linkedin_api_base_url} with user consent."
        )
