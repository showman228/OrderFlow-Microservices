import json

from redis.asyncio import Redis
from redis.exceptions import RedisError


class RedisCache:

    def __init__(self, redis_url: str, cache_ttl: int | None = None):
        self.redis = Redis.from_url(redis_url, decoded_responses=True)
        self.cache_ttl = cache_ttl

    async def set_value(self, key: str, value: dict | list) -> None:
        try:
            await self.redis.set(key, json.dumps(value), ex=self.cache_ttl)
        except RedisError:
            return

    async def get_value(self, key: str) -> dict | list | None:
        try:
            cached = await self.redis.get(key)
            if cached is None:
                return None
            return json.loads(cached)
        except RedisError:
            return None
        except json.JSONDecodeError:
            return None

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except RedisError:
            return

    async def close(self) -> None:
        await self.redis.aclose()
