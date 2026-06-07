import redis.asyncio as redis
from fastapi import Request, HTTPException
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
redis_bytes_client = redis.Redis(host=redis_host, port=6379, db=0) # For caching binary response

RATE_LIMIT = 10
RATE_LIMIT_WINDOW = 60

async def check_rate_limit(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    current_count = await redis_client.get(key)
    
    if current_count and int(current_count) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")
        
    pipe = redis_client.pipeline()
    pipe.incr(key)
    if not current_count:
        pipe.expire(key, RATE_LIMIT_WINDOW)
    await pipe.execute()
