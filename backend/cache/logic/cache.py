from backend.cache.connection import cache


def cache_set(key: str, value: str, expire: int = 3600):
    """
    Cache a value with an optional expiration time.
    @param key: key to cache
    @param value: value to cache
    @param expire: number of seconds to cache the value before expiration
    @return: True if the value was cached, False otherwise
    """
    cache.set(key, value, ex=expire)


def cache_get(key: str) -> str:
    """
    Retrieve a cached value
    @param key: key to cache
    @return: cached value
    """
    return cache.get(key)


def cache_delete(key: str):
    """
    Delete a cached value
    @param key: key to cache
    @return: True if the value was cached, False otherwise
    """
    cache.delete(key)