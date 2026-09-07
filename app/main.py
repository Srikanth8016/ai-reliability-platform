import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.alert_rules import router as alert_rules_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.incidents import router as incidents_router
from app.api.v1.logs import router as logs_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.redis_test import router as redis_router
from app.api.v1.services import router as services_router
from app.api.v1.websocket import router as websocket_router
from app.services.event_listener import listen_for_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(listen_for_events())
    yield
    task.cancel()


app = FastAPI(
    title="AI Reliability Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(services_router, prefix="/api/v1")
app.include_router(incidents_router, prefix="/api/v1")
app.include_router(logs_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(alert_rules_router, prefix="/api/v1")
app.include_router(redis_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-reliability-platform",
    }
