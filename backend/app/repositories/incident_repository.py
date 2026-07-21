from sqlalchemy.orm import Session
from app.models.incident import Incident


class IncidentRepository:

    @staticmethod
    def get_all(db: Session):
        # Order by id descending so the newest alerts appear at the top of the feed
        return db.query(Incident).order_by(Incident.id.desc()).all()

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