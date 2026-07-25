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

    @staticmethod
    def delete(db: Session, camera_id: int):
        camera = (
            db.query(Camera)
            .filter(Camera.id == camera_id)
            .first()
        )

        if camera:
            db.delete(camera)
            db.commit()

        return camera