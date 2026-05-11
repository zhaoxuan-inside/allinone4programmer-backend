from redis import asyncio as aioredis
from app.config import settings

redis_client: aioredis.Redis = None


async def init_redis():
    global redis_client
    redis_client = await aioredis.from_url(
        settings.redis_url,
        max_connections=settings.redis_max_connections,
        # 直接返回字符串，方便使用
        decode_responses=True,
    )
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()


async def get_redis() -> aioredis.Redis:
    return redis_client
