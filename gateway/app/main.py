from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import proxy
from app.middleware.logger import LoggingMiddleware
from app.auth.jwt import create_token
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middlewares
app.add_middleware(LoggingMiddleware)

# Monitoring
Instrumentator().instrument(app).expose(app)

# Routes
app.include_router(proxy.router)

@app.post("/generate-token")
def generate_token(role: str = "user"):
    token = create_token({"user": "test", "role": role})
    return {"access_token": token}
