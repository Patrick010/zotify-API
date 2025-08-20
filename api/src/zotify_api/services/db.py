from sqlalchemy import create_engine

from zotify_api.config import settings


def get_db_engine():
    if settings.database_uri:
        return create_engine(settings.database_uri)
    return None
