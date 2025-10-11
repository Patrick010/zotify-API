# ID: API-047
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from zotify_api.config import settings

if not settings.database_uri:
    raise RuntimeError(
        "DATABASE_URI must be set in the environment to use the unified database."
    )

engine = create_engine(
    settings.database_uri,
    # connect_args={"check_same_thread": False} is only needed for SQLite.
    # We will let the user handle this in their DATABASE_URI if they use SQLite.
    # e.g., "sqlite:///./zotify.db?check_same_thread=false"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Dependency ---
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session for a single request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
