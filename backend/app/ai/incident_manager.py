import asyncio
import logging
import time
from typing import Optional

from app.api.routes.ws import manager
from app.models.incident import Incident
from app.repositories.camera_repository import CameraRepository
from app.services.database_service import DatabaseService
from app.services.snapshot_service import SnapshotService
from app.services.telegram_service import TelegramService

logger = logging.getLogger("uvicorn.error")


class IncidentManager:
    COOLDOWN_SECONDS = 10
    # Class tracking cache container mapping (camera_id, incident_type) -> timestamp
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
        """
        Evaluates cooling thresholds, processes visual frames, records structural events
        to database storage, and alerts frontend clients over active websocket streams.
        """
        now = time.time()
        cooldown_key = (camera_id, incident_type)
        last = cls._last_created.get(cooldown_key)

        # 1. Enforce regional cooling threshold gates
        if last and (now - last) < cls.COOLDOWN_SECONDS:
            return None

        cls._last_created[cooldown_key] = now
        db = DatabaseService.session()

        try:
            # 2. Extract visual frame context using the internal service if provided
            snapshot_path = None
            if frame is not None:
                snapshot_path = SnapshotService.save(frame, incident_type)

            # 3. Instantiate the database model with structural metadata fields
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

            # 4. Send emergency Telegram alert
            try:
                camera = CameraRepository.get_by_id(
                    db,
                    incident.camera_id,
                )

                if camera:
                    TelegramService.send_alert(
                        incident,
                        camera,
                    )
                    logger.info(
                        "📲 Telegram alert sent for incident #%s",
                        incident.id,
                    )
                else:
                    logger.warning(
                        "⚠️ Camera details not found. Telegram alert skipped."
                    )

            except Exception as telegram_error:
                logger.exception(
                    "❌ Telegram alert failed: %s",
                    telegram_error,
                )

            # 5. Prepare the real-time event dispatch payload
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
                },
            }

            # 6. Thread-Safe WebSocket Broadcast Dispatch
            try:
                coro = manager.broadcast_json(payload)

                try:
                    # Main asynchronous event thread check
                    loop = asyncio.get_running_loop()
                    loop.create_task(coro)
                    logger.info(
                        "📡 Incident broadcast scheduled on current event loop."
                    )
                except RuntimeError:
                    # Background thread pool execution (e.g., AnyIO worker)
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.run_coroutine_threadsafe(coro, loop)
                        logger.info(
                            "📡 Incident broadcast dispatched thread-safely to main event loop."
                        )
                    else:
                        logger.warning(
                            "❌ Active event loop not found. WebSocket broadcast dropped."
                        )

            except Exception as ws_err:
                logger.error(
                    "❌ WebSocket broadcast dispatch failed: %s", ws_err
                )

            return incident

        except Exception as db_err:
            db.rollback()
            logger.error("❌ Database save transaction failed: %s", db_err)
            raise db_err
        finally:
            db.close()