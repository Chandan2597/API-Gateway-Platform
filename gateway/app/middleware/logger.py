import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("gateway")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("gateway.log")
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        log_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "method": request.method,
            "path": request.url.path,
            "latency_ms": f"{process_time:.2f}ms",
            "status_code": response.status_code
        }
        logger.info(f"{log_data['method']} {log_data['path']} {log_data['status_code']} {log_data['latency_ms']}")
        
        return response
