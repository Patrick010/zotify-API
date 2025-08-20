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
    database_uri: str = "sqlite:///./storage/zotify.db"
    redis_uri: str | None = None

    # The complex __init__ method was removed.
    # Pydantic's BaseSettings now handles loading from environment variables.
    # This fixes test failures where the test-specific API key was ignored.


settings = Settings()

# For development, if no key is provided, use a default for convenience.
if settings.app_env == "development" and not settings.admin_api_key:
    print("WARNING: No ADMIN_API_KEY set. Using default 'test_key' for development.")
    settings.admin_api_key = "test_key"

# Production check remains important.
# This logic is moved out of the class constructor to avoid side-effects.
is_prod = settings.app_env == "production"
is_missing_key = settings.require_admin_api_key_in_prod and not settings.admin_api_key
if is_prod and is_missing_key:
    # To avoid breaking existing setups, we'll check for the key file
    # that the old logic created.
    key_file_path = Path(__file__).parent.parent / ".admin_api_key"
    if key_file_path.exists():
        settings.admin_api_key = key_file_path.read_text().strip()
    else:
        # If no key is set via ENV and no key file exists, raise an error in prod.
        raise RuntimeError(
            "ADMIN_API_KEY must be set in production, "
            "and .admin_api_key file was not found."
        )
