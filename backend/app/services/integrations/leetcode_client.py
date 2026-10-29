"""Planned LeetCode integration.

Plan: read PUBLIC profile statistics (solved counts, contest badges) from
LeetCode's public GraphQL endpoint. Endpoint is configurable via
LEETCODE_API_BASE_URL. No credentials required for public data; no scraping
of anything behind login.
"""

from app.services.integrations.base import BaseIntegrationClient


class LeetCodeClient(BaseIntegrationClient):
    provider_name = "leetcode"

    def has_credentials(self) -> bool:
        # Public data only; credentials not required for the planned feature.
        return True

    def fetch(self, username: str) -> dict:
        raise NotImplementedError(
            "LeetCode sync is planned. TODO on feature/backend-sync: "
            f"POST {self.settings.leetcode_api_base_url} GraphQL query for "
            "public userProfile questions stats; verify consent/limits before "
            "enabling."
        )
