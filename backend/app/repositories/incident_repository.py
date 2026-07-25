from sqlalchemy.orm import Session
from app.models.incident import Incident


class IncidentRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Incident).order_by(Incident.id.desc()).all()

    @staticmethod
    def get_by_id(db: Session, incident_id: int):
        return (
            db.query(Incident)
            .filter(Incident.id == incident_id)
            .first()
        )

    @staticmethod
    def create(db: Session, incident: Incident):
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident

    @staticmethod
    def update_status(db: Session, incident_id: int, status: str):
        incident = (
            db.query(Incident)
            .filter(Incident.id == incident_id)
            .first()
        )

        if not incident:
            return None

        incident.status = status

        db.commit()
        db.refresh(incident)

        return incident