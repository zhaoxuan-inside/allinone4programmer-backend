from fastapi import APIRouter, Depends
from redis import asyncio as aioredis
from app.core.redis_client import get_redis

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/ping")
async def ping_redis(redis: aioredis.Redis = Depends(get_redis)):
    await redis.set("ping", "pong", ex=10)
    value = await redis.get("ping")
    return {"redis_ping": value}


@router.get("/expensive")
async def expensive_operation(redis: aioredis.Redis = Depends(get_redis)):
    cache_key = "expensive_data"
    cached = await redis.get(cache_key)
    if cached:
        return {"data": cached, "source": "cache"}

    # 模拟耗时计算（实际中可能是数据库聚合或外部 API）
    import asyncio

    await asyncio.sleep(2)
    result = "This is expensive computed data"

    await redis.set(cache_key, result, ex=60)  # 缓存 60 秒
    return {"data": result, "source": "computed"}
