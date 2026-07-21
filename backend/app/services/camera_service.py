from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.repositories.camera_repository import CameraRepository
from app.schemas.camera import CameraCreate


class CameraService:

    @staticmethod
    def list_cameras(db: Session):
        return CameraRepository.get_all(db)

    @staticmethod
    def create_camera(db: Session, data: CameraCreate):

        camera = Camera(
            name=data.name,
            stream_url=data.stream_url,
            location=data.location,
            latitude=data.latitude,
            longitude=data.longitude,
            status="online",
        )

        return CameraRepository.create(db, camera)