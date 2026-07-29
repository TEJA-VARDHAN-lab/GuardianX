import logging
from app.ai.detection_engine import DetectionEngine
from app.ai.incident_manager import IncidentManager
from app.ai.inference import InferenceEngine
from app.ai.rules_engine import RulesEngine

logger = logging.getLogger("uvicorn.error")


class DetectionService:
    FRAME_SKIP = 5
    frame_counter = 0

    @classmethod
    def process(cls, frame, camera_id: int, debug: bool = False):
        cls.frame_counter += 1
        if cls.frame_counter % cls.FRAME_SKIP != 0:
            return frame, None

        try:
            general_results, fire_results, weapon_results = InferenceEngine.detect(
                frame,
                debug=debug,
            )

            detections = []
            if general_results:
                detections.extend(
                    DetectionEngine.parse(general_results, source_name="object_model")
                )
            if fire_results:
                detections.extend(
                    DetectionEngine.parse(fire_results, source_name="fire_model")
                )
            if weapon_results:
                detections.extend(
                    DetectionEngine.parse(weapon_results, source_name="weapon_model")
                )

            incident_alert = RulesEngine.evaluate(detections)

            annotated_frame = frame.copy()
            if general_results:
                annotated_frame = general_results[0].plot(img=annotated_frame)
            if fire_results:
                annotated_frame = fire_results[0].plot(img=annotated_frame)
            if weapon_results:
                annotated_frame = weapon_results[0].plot(img=annotated_frame)

            db_incident = None
            if incident_alert:
                logger.info(
                    "🚨 %s detected (%.2f) on Camera %s",
                    incident_alert["incident_type"],
                    incident_alert["confidence"],
                    camera_id,
                )

                db_incident = IncidentManager.create(
                    camera_id=camera_id,
                    incident_type=incident_alert["incident_type"],
                    severity=incident_alert["severity"],
                    confidence=incident_alert["confidence"],
                    frame=annotated_frame,
                )

            return annotated_frame, db_incident

        except Exception as e:
            logger.exception("❌ AI pipeline failure on Camera %s: %s", camera_id, e)
            return frame, None