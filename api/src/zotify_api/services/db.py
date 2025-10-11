# ID: API-090
from typing import Optional

from sqlalchemy import Engine, create_engine

from zotify_api.config import settings


def get_db_engine() -> Optional[Engine]:
    if settings.database_uri:
        return create_engine(settings.database_uri)
    return None
