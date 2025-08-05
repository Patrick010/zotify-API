from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from zotify_api.config import settings

_engine: Optional[Engine] = None

def get_db_engine(force_recreate: bool = False) -> Optional[Engine]:
    """
    Lazily create and return a SQLAlchemy Engine.

    Returns None only if settings.database_url is falsy (shouldn't happen with dev default),
    but services must handle None gracefully for maximum safety.
    """
    global _engine
    if _engine is None or force_recreate:
        if not settings.database_url:
            return None
        _engine = create_engine(settings.database_url, future=True, echo=False)
    return _engine
