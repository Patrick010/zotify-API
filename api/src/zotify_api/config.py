import secrets
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "production"
    spotify_client_id: str = "65b708073fc0480ea92a077233ca87bd"
    admin_api_key: str | None = None
    require_admin_api_key_in_prod: bool = True
    enable_fork_features: bool = False
    feature_search_advanced: bool = False
    feature_sync_automation: bool = False
    api_prefix: str = "/api"
    database_uri: str | None = None
    redis_uri: str | None = None

    def __init__(self, key_file_path: Path | None = None, generate_key: bool = True, **values):
        super().__init__(**values)

        if not key_file_path:
            key_file_path = Path(__file__).parent.parent / ".admin_api_key"

        if self.admin_api_key:
            pass
        elif key_file_path.exists():
            self.admin_api_key = key_file_path.read_text().strip()
        elif generate_key:
            self.admin_api_key = secrets.token_hex(32)
            key_file_path.write_text(self.admin_api_key)
            os.chmod(key_file_path, 0o600)
            print(f"Generated new admin API key: {self.admin_api_key}")
            print(f"Stored in: {key_file_path}")

        if self.app_env == "production" and self.require_admin_api_key_in_prod and not self.admin_api_key:
            raise RuntimeError("ADMIN_API_KEY must be set in production.")

settings = Settings()
