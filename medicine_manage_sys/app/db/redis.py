import aioredis


async def redis_pool():
    redis = aioredis.from_url(url="redis://192.168.43.113", port=6379, password="root", db=0, encoding="utf-8",
                              decode_responses=True)
    return redis
