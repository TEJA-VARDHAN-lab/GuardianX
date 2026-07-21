from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.api.routes.camera import router as camera_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.incident import router as incident_router
from app.api.routes.stream import router as stream_router
from app.api.routes.ws import router as ws_router
from app.core.config import settings
from app.db.database import Base, engine
from fastapi.staticfiles import StaticFiles

# Ensure DB initialization is stable
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
)

app.mount("/snapshots", StaticFiles(directory="snapshots"), name="snapshots")

# Standard HTTP CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration mapping sequence
app.include_router(health_router)
app.include_router(camera_router, prefix="/api/v1")
app.include_router(incident_router)
app.include_router(dashboard_router)
app.include_router(stream_router, prefix="/api/v1/cameras")
app.include_router(ws_router) 

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "GuardianX API",
        "version": settings.API_VERSION,
    }