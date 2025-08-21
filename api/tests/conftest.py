from typing import Any, Dict, List, Optional, Tuple

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zotify_api.config import Settings
from zotify_api.database.session import Base
from zotify_api.main import app
from zotify_api.providers.base import BaseProvider
from zotify_api.services.deps import get_provider, get_settings


@pytest.fixture
def client():
    """
    A TestClient instance that can be used in all tests.
    It has the authentication dependency overridden to use a static test API key.
    This fixture is function-scoped to ensure test isolation.
    """

    def get_settings_override():
        # Use app_env='testing' to match the pytest commandline argument
        return Settings(admin_api_key="test_key", app_env="testing")

    # Apply the override
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as c:
        yield c

    # Clear all overrides after the test has run
    app.dependency_overrides.clear()


class FakeProvider(BaseProvider):
    """
    A mock provider for testing purposes.
    Implements the BaseProvider interface and returns mock data.
    """

    async def search(
        self, q: str, type: str, limit: int, offset: int
    ) -> Tuple[List[Dict[str, Any]], int]:
        return [{"id": "test_track"}], 1

    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        return {"id": playlist_id, "name": "Test Playlist"}

    async def get_playlist_tracks(
        self, playlist_id: str, limit: int, offset: int
    ) -> Dict[str, Any]:
        return {"items": [{"track": {"id": "test_track"}}]}

    async def sync_playlists(self) -> Dict[str, Any]:
        return {"status": "success", "count": 1}

    async def get_oauth_login_url(self, state: str) -> str:
        return f"http://fake.provider.com/login?state={state}"

    async def handle_oauth_callback(
        self, code: Optional[str], error: Optional[str], state: str
    ) -> str:
        if error:
            return f"<html><body>Error: {error}</body></html>"
        return "<html><body>Success</body></html>"


@pytest.fixture
def mock_provider(monkeypatch):
    """
    Fixture to override the get_provider dependency with the FakeProvider.
    """
    fake_provider = FakeProvider()
    app.dependency_overrides[get_provider] = lambda: fake_provider
    yield fake_provider
    del app.dependency_overrides[get_provider]

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="function")
def test_db_session():
    """
    Pytest fixture to set up a new in-memory SQLite database for each test function.
    It creates a single connection for the test's duration, creates all tables on
    that connection, and yields a session bound to it. This pattern is crucial
    for ensuring the in-memory database persists across the test function.
    """
    # Import models here to ensure they are registered with Base.metadata
    # before create_all is called.

    # A single connection is held for the duration of the test
    connection = engine.connect()

    # Begin a transaction
    transaction = connection.begin()

    # Create the tables on this connection
    Base.metadata.create_all(bind=connection)

    # Bind the session to this specific connection
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=connection
    )
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Rollback the transaction to ensure test isolation
        transaction.rollback()
        # Close the connection
        connection.close()
