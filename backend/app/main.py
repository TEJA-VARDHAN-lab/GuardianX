import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import app.models
from app.api.routes import assistant
from app.api.routes.assistant import router as assistant_router
from app.api.routes.camera import router as camera_router
from app.api.routes.camera_stream import router as camera_stream_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.health_camera import router as camera_health_router
from app.api.routes.incident import router as incident_router
from app.api.routes.stream import router as stream_router
from app.api.routes.ws import router as ws_router
from app.camera.registry import CameraRegistry
from app.core.config import settings
from app.db.database import Base, engine
from app.models.camera import Camera
from app.services.database_service import DatabaseService

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DatabaseService.session()
    try:
        cameras = db.query(Camera).all()

        if not cameras:
            default_camera = Camera(
                name="Camera 1",
                location="Main Entrance Hallway",
                location_name="Main Entrance",
                latitude=17.385044,
                longitude=78.486671,
                source="0",
                status="online",
            )
            db.add(default_camera)
            db.commit()
            db.refresh(default_camera)
            cameras = [default_camera]
            print(f"🌱 Seeded default Camera ID {default_camera.id} (Source: {default_camera.source})")

        for camera in cameras:
            worker = CameraRegistry.add(camera.id, camera.source)
            if worker and not worker.running:
                worker.start()

        print("ACTIVE CAMERA WORKERS:", list(CameraRegistry.workers.keys()))
    finally:
        db.close()

    yield

    for camera_id in list(CameraRegistry.workers.keys()):
        CameraRegistry.remove(camera_id)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("snapshots", exist_ok=True)
app.mount("/snapshots", StaticFiles(directory="snapshots"), name="snapshots")

app.include_router(health_router)
app.include_router(camera_router)
app.include_router(camera_health_router)
app.include_router(incident_router)
app.include_router(dashboard_router)
app.include_router(stream_router, prefix="/api/v1/cameras")
app.include_router(ws_router)
app.include_router(camera_stream_router)
app.include_router(assistant.router)

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("🔌 Client disconnected from WebSocket cleanly")

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "GuardianX API",
        "version": settings.API_VERSION,
    }