import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.config import Settings
from zotify_api.services.deps import get_settings


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
