import redis
from datetime import datetime
from zotify_api.config import settings

def get_cache_stats(redis_client=None):
    if settings.cache_type == "redis" and settings.redis_url:
        r = redis_client or redis.from_url(settings.redis_url)
        info = r.info()
        total_items = r.dbsize()
        # memory usage: use info if available
        memory_usage = info.get("used_memory", 0) / (1024*1024)
        # hit_rate: Redis INFO provides keyspace hits/misses
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        hit_rate = (hits / (hits + misses) * 100) if (hits + misses) > 0 else 0.0
        last_cleared = None  # Could be kept in a key if you maintain it
        return {
            "total_items": int(total_items),
            "memory_usage_mb": round(memory_usage, 2),
            "hit_rate": round(hit_rate, 2),
            "last_cleared": last_cleared
        }
    # fallback: in-memory cache (if you have counters)
    return {"total_items": 0, "memory_usage_mb": 0.0, "hit_rate": 0.0, "last_cleared": None}
