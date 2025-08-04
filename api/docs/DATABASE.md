Zotify API Database Configuration

The Zotify API is designed to be flexible and allows you to easily switch from the default JSON file-based storage to a more robust database system like SQLite, PostgreSQL, or MariaDB. This is made possible by FastAPI's dependency injection system.
How It Works

The entire API interacts with the database through a single dependency function: get_db() located in api/src/zotify_api/database.py.

API routes declare their need for a database like this:

from zotify_api import database

@router.get("/playlists")
async def get_playlists(db: List[dict] = Depends(database.get_db)):
    # The 'db' variable is provided by FastAPI
    return db

To change the database backend for the entire application, you only need to modify the get_db and save_db functions in api/src/zotify_api/database.py. The API route code does not need to be touched.
Example: Switching to SQLite

Here is a conceptual example of how you could modify database.py to use a relational database like SQLite.

1. Install the required driver:

pip install sqlalchemy

2. Update database.py:

You would change the contents of database.py to manage a real database session. The key is that the get_db function would yield a session, and the save_db logic would be handled by db.commit().

# api/src/zotify_api/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# You would also need to define your SQLAlchemy models here
# from . import models

# 1. Configure your database connection
DATABASE_URL = "sqlite:///./zotify.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
# models.Base.metadata.create_all(bind=engine)


# 2. Create the dependency function
def get_db():
    """
    FastAPI dependency that provides a database session.
    It ensures the database connection is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Update your route logic to use the new session
#    You would no longer need a separate 'save_db' function.
#    You would call db.commit(), db.add(), db.refresh() etc.

3. Update an example route:

Your route functions would now receive a SQLAlchemy Session object instead of a list.

from sqlalchemy.orm import Session

@router.post("/playlists")
async def create_playlist(playlist_in: PlaylistCreate, db: Session = Depends(database.get_db)):
    # Create a SQLAlchemy model instance
    new_playlist = models.Playlist(name=playlist_in.name)

    # Add, commit, and refresh
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)

    return new_playlist

By centralizing the database logic behind the get_db dependency, the API becomes incredibly flexible. You can follow a similar pattern for PostgreSQL or MariaDB by installing their respective drivers (e.g., psycopg2 or mysqlclient) and changing the DATABASE_URL.
