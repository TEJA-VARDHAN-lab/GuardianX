from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.websocket.manager import manager


class IncidentService:

    @staticmethod
    def list_incidents(db: Session):
        return IncidentRepository.get_all(db)

    @staticmethod
    def create_incident(db: Session, data: IncidentCreate):
        incident = Incident(
            camera_id=data.camera_id,
            incident_type=data.incident_type,
            severity=data.severity,
            confidence=data.confidence,
            status="detected",
        )

        incident = IncidentRepository.create(db, incident)

        # Broadcast the initial incident creation event to active connections
        manager.broadcast_json(
            {
                "event": "incident.created",
                "payload": {
                    "id": incident.id,
                    "camera_id": incident.camera_id,
                    "incident_type": incident.incident_type,
                    "severity": incident.severity,
                    "confidence": incident.confidence,
                    "status": incident.status,
                    "created_at": incident.created_at.isoformat()
                    if incident.created_at
                    else None,
                },
            }
        )

        return incident
        
    @staticmethod
    def update_status(db: Session, incident_id: int, status: str):
        # 1. Update the record in the database
        incident = IncidentRepository.update_status(
            db,
            incident_id,
            status,
        )

        # 2. If the incident exists, broadcast the status change over WebSockets
        if incident:
            manager.broadcast_json(
                {
                    "event": "incident.updated",
                    "payload": {
                        "id": incident.id,
                        "status": incident.status,
                    },
                }
            )

        return incident