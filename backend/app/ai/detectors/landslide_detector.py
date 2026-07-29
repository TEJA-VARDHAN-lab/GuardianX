import logging


logger = logging.getLogger("uvicorn.error")


class LandslideDetector:

    LANDSLIDE_CLASSES = {
        "rock",
        "debris",
        "rubble",
        "mud",
        "landslide",
    }


    @classmethod
    def evaluate(cls, detections):

        for detection in detections:

            label = detection.class_name.lower()


            if (
                label in cls.LANDSLIDE_CLASSES
                and detection.confidence >= 0.60
            ):

                logger.info(
                    "⛰️ Landslide condition detected confidence=%.2f",
                    detection.confidence
                )

                return {
                    "incident_type": "landslide",
                    "severity": "critical",
                    "confidence": detection.confidence,
                }


        return None