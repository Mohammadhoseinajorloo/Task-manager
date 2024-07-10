from backend.core.config import settings
from redis import Redis


def get_redis_connection(**kwargs) -> Redis:
    if "decode_responses" not in kwargs:
        kwargs["decode_responses"] = True

    # If someone passed in a 'url' parameter, or specified a REDIS_OM_URL
    # environment variable, we'll create the Redis client from the URL.
    url = kwargs.pop("url", settings.CACHE_URL)
    if url:
        return Redis.from_url(url, **kwargs)
    return Redis(**kwargs)
