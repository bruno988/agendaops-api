import json
from typing import Any

import redis

from agendaops.core.config import get_settings

settings = get_settings()
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_cache(key: str) -> Any | None:
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def set_cache(key: str, value: Any, ttl: int = 60) -> None:
    redis_client.setex(key, ttl, json.dumps(value))


def delete_cache(key: str) -> None:
    redis_client.delete(key)