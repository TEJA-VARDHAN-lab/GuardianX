from fastapi import APIRouter

from app.camera.registry import CameraRegistry


router = APIRouter(
    prefix="/api/v1/camera-health",
    tags=["Camera Health"],
)


@router.get("")
def get_camera_health():

    return [
        worker.health()
        for worker in CameraRegistry.workers.values()
    ]