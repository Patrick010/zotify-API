from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str
    redis_url: str | None = None
    log_file_path: str = "/var/log/zotify/app.log"
    library_path: str = "/srv/media/library"
    app_version: str = "0.0.1"
    cache_type: str = "inmemory"

    class Config:
        env_file = ".env"

settings = Settings()
