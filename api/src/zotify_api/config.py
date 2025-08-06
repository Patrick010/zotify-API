from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "production"
    admin_api_key: str | None = None
    require_admin_api_key_in_prod: bool = True
    enable_fork_features: bool = False
    feature_search_advanced: bool = False
    feature_sync_automation: bool = False
    api_prefix: str = "/api"
    database_uri: str | None = None
    redis_uri: str | None = None

    def __post_init__(self):
        if self.app_env == "production" and self.require_admin_api_key_in_prod and not self.admin_api_key:
            raise RuntimeError("ADMIN_API_KEY must be set in production.")

settings = Settings()
