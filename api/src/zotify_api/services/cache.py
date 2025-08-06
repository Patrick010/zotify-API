import redis
from zotify_api.config import settings

def get_redis_client():
    if settings.redis_uri:
        return redis.from_url(settings.redis_uri)
    return None

def cache_get(key):
    client = get_redis_client()
    if client:
        return client.get(key)
    return None

def cache_set(key, value, ttl):
    client = get_redis_client()
    if client:
        client.set(key, value, ex=ttl)
