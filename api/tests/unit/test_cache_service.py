import pytest

from zotify_api.services.cache_service import CacheService


@pytest.fixture
def cache_state():
    return {
        "search": 80,
        "metadata": 222
    }

def test_get_cache_status(cache_state):
    service = CacheService(cache_state)
    status = service.get_cache_status()
    assert status["total_items"] == 302
    assert status["by_type"] == cache_state

def test_clear_cache_all(cache_state):
    service = CacheService(cache_state)
    result = service.clear_cache()
    assert result["total_items"] == 0

def test_clear_cache_by_type(cache_state):
    service = CacheService(cache_state)
    result = service.clear_cache("search")
    assert result["by_type"]["search"] == 0
    assert result["by_type"]["metadata"] == 222

def test_clear_cache_invalid_type(cache_state):
    service = CacheService(cache_state)
    result = service.clear_cache("invalid")
    assert result["total_items"] == 302
