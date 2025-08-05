from sqlalchemy import create_engine, text

from zotify_api.config import settings

def main():
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE tracks (id TEXT PRIMARY KEY, name TEXT, updated_at TEXT)"))
        conn.execute(text("CREATE TABLE playlists (id TEXT PRIMARY KEY, name TEXT, updated_at TEXT)"))
        conn.commit()

if __name__ == "__main__":
    main()
