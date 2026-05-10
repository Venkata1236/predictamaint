from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import app_logger
from app.routes.analyze import router as analyze_router
from app.routes.websocket import (
    router as websocket_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    analyze_router,
    prefix="/api/v1",
    tags=["Analysis"],
)

app.include_router(
    websocket_router
)

@app.on_event("startup")
async def startup_event():
    app_logger.info("Starting PredictaMaint API")


@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Shutting down PredictaMaint API")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    return {
        "message": "PredictaMaint API is running"
    }