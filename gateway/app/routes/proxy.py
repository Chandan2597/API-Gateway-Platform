from fastapi import APIRouter, Request, HTTPException, Depends, Response
from app.discovery.registry import SERVICES
from app.auth.jwt import verify_token
from app.auth.rbac import check_permissions
from app.middleware.rate_limit import check_rate_limit
from app.middleware.cache import get_cached_response, set_cached_response
import httpx

router = APIRouter()

client = httpx.AsyncClient()

async def forward_request(method: str, url: str, content: bytes, headers: dict):
    response = await client.request(method, url, content=content, headers=headers)
    return response

@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(service: str, path: str, request: Request, user_payload: dict = Depends(verify_token)):
    await check_rate_limit(request)
    check_permissions(user_payload, request.method, path)
    
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
        
    target_url = f"{SERVICES[service]}/{path}"
    
    cached_response = await get_cached_response(request)
    if cached_response:
        return cached_response
        
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    try:
        response = await forward_request(
            method=request.method,
            url=target_url,
            content=body,
            headers=headers
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Bad Gateway: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if response.status_code == 200:
        await set_cached_response(request, response.content)
        
    # Prepare response headers to forward to client, filter out some to avoid issues
    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    response_headers = {k: v for k, v in response.headers.items() if k.lower() not in excluded_headers}

    return Response(content=response.content, status_code=response.status_code, headers=response_headers)
