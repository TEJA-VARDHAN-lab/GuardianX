from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.repositories.camera_repository import CameraRepository
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.services.telegram_service import TelegramService
from app.websocket.manager import manager


class IncidentService:

    @staticmethod
    def get_incident(db: Session, incident_id: int):
        return IncidentRepository.get_by_id(db, incident_id)

    @staticmethod
    def list_incidents(db: Session):
        return IncidentRepository.get_all(db)

    @staticmethod
    async def create_incident(db: Session, data: IncidentCreate):
        # 1. Save incident to database
        incident = Incident(
            camera_id=data.camera_id,
            incident_type=data.incident_type,
            severity=data.severity,
            confidence=data.confidence,
            status="detected",
        )
        incident = IncidentRepository.create(db, incident)

        # 2. Fetch associated camera details for alert metadata
        camera = CameraRepository.get_by_id(db, incident.camera_id)

        # 3. Broadcast real-time update to web dashboard via WebSockets
        await manager.broadcast_json(
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

        # 4. 🚨 Send Telegram push notification
        if camera:
            print("🚨 CALLING TELEGRAM ALERT")
            TelegramService.send_alert(incident, camera)

        # 5. 📷 Send snapshot photo to Telegram if available
        if hasattr(incident, "snapshot") and incident.snapshot:
            TelegramService.send_photo(
                photo=incident.snapshot,
                caption=f"📷 Incident #{incident.id} Snapshot",
            )

        return incident

    @staticmethod
    async def update_status(db: Session, incident_id: int, status: str):
        incident = IncidentRepository.update_status(db, incident_id, status)

        if incident:
            await manager.broadcast_json(
                {
                    "event": "incident.updated",
                    "payload": {
                        "id": incident.id,
                        "status": incident.status,
                    },
                }
            )

        return incident