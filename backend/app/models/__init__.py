"""SQLAlchemy ORM models.

Third-party (synced) data is stored separately from user-approved resume
data: `Profile` holds only data the user approved via PUT /api/profile,
while `ExternalProfileSnapshot` holds raw payloads fetched by future
integrations without touching the approved profile.
"""

from app.models.profile import Profile
from app.models.sync_history import ExternalProfileSnapshot, SyncHistory

__all__ = ["Profile", "ExternalProfileSnapshot", "SyncHistory"]
