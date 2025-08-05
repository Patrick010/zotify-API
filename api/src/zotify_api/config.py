# api/src/zotify_api/config.py
import os
import logging
from pydantic_settings import BaseSettings

log = logging.getLogger(__name__)

class Settings(BaseSettings):
    # "development" | "staging" | "production"
    app_env: str = "development"

    # Dev-friendly default so app boots without DB. Can be overridden by env/.env.
    database_url: str = "sqlite:///./dev.db"

    redis_url: str | None = None
    log_file_path: str = "/var/log/zotify/app.log"
    library_path: str = "/srv/media/library"
    app_version: str = "0.0.1"
    cache_type: str = "inmemory"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Production safety: require DATABASE_URL explicitly when app_env=production.
if settings.app_env.lower() == "production":
    # Note: prefer to check raw env var so explicit override is required in prod.
    if not os.environ.get("DATABASE_URL"):
        log.error("DATABASE_URL is required in production but not set. Aborting startup.")
        raise RuntimeError("DATABASE_URL environment variable is required in production")
