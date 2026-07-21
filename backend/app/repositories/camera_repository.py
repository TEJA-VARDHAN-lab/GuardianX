from sqlalchemy.orm import Session
from app.models.camera import Camera


class CameraRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Camera).all()

    @staticmethod
    def create(db: Session, camera: Camera):
        db.add(camera)
        db.commit()
        db.refresh(camera)
        return camera