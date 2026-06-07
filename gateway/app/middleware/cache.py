from fastapi import Request, Response
from app.middleware.rate_limit import redis_bytes_client

CACHE_TTL = 60

async def get_cached_response(request: Request):
    if request.method != "GET":
        return None
        
    cache_key = f"cache:{request.url.path}"
    cached_data = await redis_bytes_client.get(cache_key)
    if cached_data:
        return Response(content=cached_data, media_type="application/json")
    return None

async def set_cached_response(request: Request, content: bytes):
    if request.method == "GET":
        cache_key = f"cache:{request.url.path}"
        await redis_bytes_client.set(cache_key, content, ex=CACHE_TTL)
