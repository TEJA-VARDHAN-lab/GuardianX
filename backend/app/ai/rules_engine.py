import logging

from app.ai.detection_engine import Detection


logger = logging.getLogger("uvicorn.error")


class RulesEngine:

    FIRE_THRESHOLD = 0.30
    SMOKE_THRESHOLD = 0.30


    @staticmethod
    def evaluate(
        detections: list[Detection]
    ):

        for detection in detections:

            label = detection.class_name.lower()


            # Fire emergency rule
            if (
                label == "fire"
                and detection.confidence >= RulesEngine.FIRE_THRESHOLD
            ):

                logger.info(
                    "🔥 Fire accepted confidence=%s",
                    detection.confidence
                )

                return {
                    "incident_type": "fire",
                    "severity": "high",
                    "confidence": detection.confidence,
                }


            # Smoke emergency rule
            if (
                label == "smoke"
                and detection.confidence >= RulesEngine.SMOKE_THRESHOLD
            ):

                logger.info(
                    "💨 Smoke accepted confidence=%s",
                    detection.confidence
                )

                return {
                    "incident_type": "smoke",
                    "severity": "high",
                    "confidence": detection.confidence,
                }


            # Normal objects are ignored
            logger.info(
                "Object detected but ignored: %s %.2f",
                label,
                detection.confidence
            )


        return None