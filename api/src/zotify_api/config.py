import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    version: str = "0.1.0"
    app_env: str = "production"
    admin_api_key: str | None = None
    require_admin_api_key_in_prod: bool = True
    enable_fork_features: bool = False
    feature_search_advanced: bool = False
    feature_sync_automation: bool = False
    api_prefix: str = "/api"
    database_uri: str | None = None
    redis_uri: str | None = None

    # The complex __init__ method was removed.
    # Pydantic's BaseSettings will now handle loading from environment variables directly.
    # This fixes the test failures where the test-specific API key was being ignored.

settings = Settings()

# Production check remains important.
# This logic is moved out of the class constructor to avoid side-effects during instantiation.
if settings.app_env == "production" and settings.require_admin_api_key_in_prod and not settings.admin_api_key:
    # To avoid breaking existing setups, we'll check for the key file that the old logic created.
    key_file_path = Path(__file__).parent.parent / ".admin_api_key"
    if key_file_path.exists():
        settings.admin_api_key = key_file_path.read_text().strip()
    else:
        # If no key is set via ENV and no key file exists, raise an error in prod.
        raise RuntimeError("ADMIN_API_KEY must be set in production, and .admin_api_key file was not found.")
