import datetime
from redis_om import JsonModel
from backend.cache.connection import redis


class CacheTask(JsonModel):
    title: str
    description: str
    date: datetime.date
    owner_id: int
    owner_name: str
    is_done: bool
    is_active: bool

    class Config:
        database = redis
