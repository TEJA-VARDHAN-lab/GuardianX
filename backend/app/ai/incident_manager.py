import asyncio
import logging
import time
from typing import Optional

from app.models.camera import Camera
from app.models.incident import Incident
from app.repositories.camera_repository import CameraRepository
from app.services.alert_message_service import AlertMessageService
from app.services.database_service import DatabaseService
from app.services.emergency_router import EmergencyRouter
from app.services.notification_dispatcher import NotificationDispatcher
from app.services.snapshot_service import SnapshotService
from app.services.telegram_service import TelegramService
from app.services.websocket_manager import manager

logger = logging.getLogger("uvicorn.error")


def run_async_coro(coro):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(coro)
    except RuntimeError:
        try:
            asyncio.run(coro)
        except Exception as err:
            logger.error("❌ Failed to run async task in background thread: %s", err)


class IncidentManager:
    COOLDOWN_SECONDS = 10
    _last_created: dict[tuple[int, str], float] = {}

    @classmethod
    def create(
        cls,
        camera_id: int,
        incident_type: str,
        severity: str,
        confidence: float,
        frame=None,
    ) -> Optional[Incident]:
        now = time.time()
        cooldown_key = (camera_id, incident_type)
        last = cls._last_created.get(cooldown_key)

        if last and (now - last) < cls.COOLDOWN_SECONDS:
            return None

        cls._last_created[cooldown_key] = now
        db = DatabaseService.session()

        try:
            snapshot_path = None
            if frame is not None:
                snapshot_path = SnapshotService.save(frame, incident_type)

            incident = Incident(
                camera_id=camera_id,
                incident_type=incident_type,
                severity=severity,
                confidence=confidence,
                status="detected",
                snapshot=snapshot_path,
            )

            db.add(incident)
            db.commit()
            db.refresh(incident)

            logger.info(
                "✅ Incident #%s created (%s) on Camera %s",
                incident.id,
                incident.incident_type,
                incident.camera_id,
            )

            departments = []
            try:
                departments = EmergencyRouter.get_departments(incident.incident_type)
                if isinstance(departments, str):
                    departments = [departments]

                logger.info("🚑 Dispatch Required: %s", departments)

                message = AlertMessageService.generate(incident)

                for department in departments:
                    try:
                        NotificationDispatcher.send(department, message, incident.snapshot)
                        logger.info("📢 Notification sent to department: %s", department)
                    except Exception as notify_err:
                        logger.error(
                            "❌ Failed to dispatch notification to %s: %s",
                            department,
                            notify_err,
                        )
            except Exception as router_err:
                logger.error("❌ Emergency router error: %s", router_err)

            try:
                camera = None
                if hasattr(CameraRepository, "get_by_id"):
                    camera = CameraRepository.get_by_id(db, incident.camera_id)
                elif hasattr(CameraRepository, "get"):
                    camera = CameraRepository.get(db, incident.camera_id)
                else:
                    camera = db.query(Camera).filter(Camera.id == incident.camera_id).first()

                if camera:
                    run_async_coro(TelegramService.send_alert(incident, camera))
                    logger.info("📲 Telegram alert dispatched for incident #%s", incident.id)
                else:
                    logger.warning(
                        "⚠️ Camera #%s not found in database. Telegram alert skipped.",
                        incident.camera_id,
                    )
            except Exception as telegram_error:
                logger.exception("❌ Telegram alert failed: %s", telegram_error)

            payload = {
                "event": "incident.created",
                "incident": {
                    "id": incident.id,
                    "camera_id": incident.camera_id,
                    "incident_type": incident.incident_type,
                    "severity": incident.severity,
                    "confidence": incident.confidence,
                    "status": incident.status,
                    "snapshot": incident.snapshot,
                    "departments": departments,
                },
            }

            try:
                run_async_coro(manager.broadcast_json(payload))
                logger.info("📡 WebSocket broadcast scheduled safely.")
            except Exception as ws_err:
                logger.error("❌ WebSocket broadcast dispatch failed: %s", ws_err)

            return incident

        except Exception as db_err:
            db.rollback()
            logger.error("❌ Database save transaction failed: %s", db_err)
            raise
        finally:
            db.close()