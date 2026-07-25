from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.repositories.camera_repository import CameraRepository
from app.schemas.camera import CameraCreate


class CameraService:

    @staticmethod
    def list_cameras(db: Session):
        return CameraRepository.get_all(db)

    @staticmethod
    def create_camera(
        db: Session,
        data: CameraCreate,
    ):
        camera = Camera(
            name=data.name,
            location=data.location,
            location_name=data.location_name,
            latitude=data.latitude,
            longitude=data.longitude,
            source=data.source,
            status="offline",
            ai_enabled=True,
        )

        return CameraRepository.create(db, camera)

    @staticmethod
    def delete_camera(
        db: Session,
        camera_id: int,
    ):
        return CameraRepository.delete(db, camera_id)