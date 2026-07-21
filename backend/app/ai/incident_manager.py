import logging
import time
import asyncio
from typing import Optional

from app.models.incident import Incident
from app.services.database_service import DatabaseService
from app.api.routes.ws import manager
from app.services.snapshot_service import SnapshotService

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
        frame=None,  # 🚀 Added optional default block support
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
                # 🧠 Fix: Moved the snapshot execution safely inside the method scope
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
            
            # 4. Prepare the real-time event dispatch payload
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

            # 5. Thread-Safe WebSocket Broadcast Dispatch
            try:
                coro = manager.broadcast_json(payload)
                
                try:
                    # If executing on the main asynchronous event thread, register immediately
                    loop = asyncio.get_running_loop()
                    loop.create_task(coro)
                    logger.info("📡 Incident broadcast scheduled on current event loop.")
                except RuntimeError:
                    # Executing inside a synchronous background worker thread pool (e.g., AnyIO worker).
                    # Safely schedule the coroutine onto the running main application event loop thread.
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.run_coroutine_threadsafe(coro, loop)
                        logger.info("📡 Incident broadcast dispatched thread-safely to main event loop.")
                    else:
                        logger.warning("❌ Active event loop not found. WebSocket broadcast dropped.")
                        
            except Exception as ws_err:
                logger.error("❌ WebSocket broadcast dispatch failed: %s", ws_err)

            return incident

        except Exception as db_err:
            db.rollback()
            logger.error("❌ Database save transaction failed: %s", db_err)
            raise db_err
        finally:
            db.close()