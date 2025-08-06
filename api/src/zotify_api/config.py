from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    admin_api_key: str | None = None
    enable_fork_features: bool = False
    feature_search_advanced: bool = False
    feature_sync_automation: bool = False
    api_prefix: str = "/api"
    database_uri: str | None = None
    redis_uri: str | None = None

settings = Settings()
