"""
Cache service module.

This module contains the business logic for the cache subsystem.
The functions in this module are designed to be called from the API layer.
"""
from typing import Any, Dict, Optional


class CacheService:
    def __init__(self, cache_state: Dict[str, Any]):
        self._cache_state = cache_state

    def get_cache_status(self) -> Dict[str, Any]:
        return {
            "total_items": sum(self._cache_state.values()),
            "by_type": self._cache_state
        }

    def clear_cache(self, cache_type: Optional[str] = None) -> Dict[str, Any]:
        if cache_type:
            if cache_type in self._cache_state:
                self._cache_state[cache_type] = 0
        else:
            for k in self._cache_state:
                self._cache_state[k] = 0
        return self.get_cache_status()

def get_cache_service():
    # This is a placeholder for a real implementation that would get the cache state from a persistent storage.
    cache_state = {
        "search": 80,
        "metadata": 222
    }
    return CacheService(cache_state)
