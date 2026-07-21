from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.camera import CameraCreate, CameraResponse
from app.services.camera_service import CameraService

router = APIRouter(prefix="/api/v1/cameras", tags=["Cameras"])

@router.get("", response_model=list[CameraResponse])
def get_cameras(db: Session = Depends(get_db)):
    return CameraService.list_cameras(db)

@router.post("", response_model=CameraResponse)
def create_camera(
    camera: CameraCreate,
    db: Session = Depends(get_db),
):
    return CameraService.create_camera(db, camera)