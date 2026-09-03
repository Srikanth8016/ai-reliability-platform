from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.alert_rules import router as alert_rules_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.incidents import router as incidents_router
from app.api.v1.logs import router as logs_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.services import router as services_router

app = FastAPI(
    title="AI Reliability Platform",
    version="1.0.0",
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

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    services_router,
    prefix="/api/v1",
)

app.include_router(
    incidents_router,
    prefix="/api/v1",
)

app.include_router(
    logs_router,
    prefix="/api/v1",
)

app.include_router(
    metrics_router,
    prefix="/api/v1",
)

app.include_router(
    alerts_router,
    prefix="/api/v1",
)

app.include_router(
    alert_rules_router,
    prefix="/api/v1",
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-reliability-platform",
    }
