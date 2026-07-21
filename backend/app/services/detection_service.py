import logging

from app.ai.detection_engine import DetectionEngine
from app.ai.inference import InferenceEngine
from app.ai.rules_engine import RulesEngine
from app.ai.incident_manager import IncidentManager

logger = logging.getLogger("uvicorn.error")


class DetectionService:
    """
    Runs the complete AI detection pipeline for a camera video frame.
    """

    @staticmethod
    def process(frame, camera_id: int):
        """
        Processes a raw frame through inference, parses detections, checks rule violations,
        and persists/broadcasts incidents if triggered.

        Returns:
            annotated_frame (numpy.ndarray): The visual frame with drawn bounding boxes.
            db_incident (Incident or None): The verified database model instance if created.
        """
        try:
            # 1. Run raw ML inference model matching (receives explicit tuple output)
            general_results, fire_results = InferenceEngine.detect(frame)

            # ===== DEBUG START =====
            # Fix: Merged result list check for logging purposes
            has_general = general_results and len(general_results) > 0
            has_fire = fire_results and len(fire_results) > 0

            if has_general or has_fire:
                if has_general:
                    logger.info("📋 General Model names: %s", getattr(general_results[0], "names", "Unknown"))
                    if hasattr(general_results[0], "boxes"):
                        logger.info("📦 General Boxes detected: %s", len(general_results[0].boxes))
                if has_fire:
                    logger.info("📋 Fire Model names: %s", getattr(fire_results[0], "names", "Unknown"))
                    if hasattr(fire_results[0], "boxes"):
                        logger.info("🔥 Fire/Smoke Boxes detected: %s", len(fire_results[0].boxes))
            else:
                logger.warning("⚠️ No frame result objects returned from either model network.")
            # ===== DEBUG END =====

            # Fix: Safely indented the detection extraction pipeline
            general_detections = DetectionEngine.parse(general_results)
            fire_detections = DetectionEngine.parse(fire_results)
            detections = general_detections + fire_detections
            
            logger.info("🧠 AI detections parsed: %s", detections)

            # 2. Check targets against custom thresholds and severity matrices
            incident_alert = RulesEngine.evaluate(detections)

            # 3. Handle visual box plotting overlays sequentially to merge drawings
            annotated_frame = frame

            if general_results and len(general_results) > 0:
                annotated_frame = general_results[0].plot()

            if fire_results and len(fire_results) > 0:
                # Passes existing annotated_frame context to draw right over the general detections
                annotated_frame = fire_results[0].plot(img=annotated_frame)

            # 4. Handle persistence if an alert state was triggered
            db_incident = None
            if incident_alert:
                logger.info(
                    "🚨 %s detected (%.2f) on Camera %s",
                    incident_alert["incident_type"],
                    incident_alert["confidence"],
                    camera_id,
                )
                logger.info("Forwarding payload parameters to IncidentManager context...")

                db_incident = IncidentManager.create(
                    camera_id=camera_id,
                    incident_type=incident_alert["incident_type"],
                    severity=incident_alert["severity"],
                    confidence=incident_alert["confidence"],
                    frame=annotated_frame, 
                )

            return annotated_frame, db_incident

        except Exception as e:
            logger.exception("❌ AI pipeline processing failed for Camera %s: %s", camera_id, e)
            return frame, None