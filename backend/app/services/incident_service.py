import logging
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.repositories.camera_repository import CameraRepository
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.services.telegram_service import TelegramService
from app.websocket.manager import manager

logger = logging.getLogger("uvicorn.error")


class IncidentService:
    @staticmethod
    def get_incident(db: Session, incident_id: int):
        return IncidentRepository.get_by_id(db, incident_id)

    @staticmethod
    def list_incidents(db: Session):
        return IncidentRepository.get_all(db)

    @staticmethod
    async def create_incident(db: Session, data: IncidentCreate):
        snapshot_val = getattr(data, "snapshot", None)

        incident = Incident(
            camera_id=data.camera_id,
            incident_type=data.incident_type,
            severity=data.severity,
            confidence=data.confidence,
            status="detected",
            snapshot=snapshot_val,
        )
        incident = IncidentRepository.create(db, incident)
        camera = CameraRepository.get_by_id(db, incident.camera_id)

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
                    "created_at": incident.created_at.isoformat() if getattr(incident, "created_at", None) else None,
                },
            }
        )

        if camera:
            try:
                message = (
                    f"🚨 Incident #{incident.id}\n"
                    f"Type: {incident.incident_type}\n"
                    f"Severity: {incident.severity}\n"
                    f"Confidence: {incident.confidence}"
                )
                TelegramService.send_alert(message, image_path=snapshot_val)
            except Exception as e:
                logger.error("❌ Telegram notification error on create: %s", e)
        else:
            logger.warning("⚠️ Camera #%s not found. Telegram skipped.", incident.camera_id)

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

            try:
                camera = CameraRepository.get_by_id(db, incident.camera_id)
                if camera:
                    message = (
                        f"🚨 Incident #{incident.id} updated\n"
                        f"New status: {status}"
                    )
                    TelegramService.send_alert(message)
            except Exception as e:
                logger.error("❌ Telegram notification error on update: %s", e)

        return incident