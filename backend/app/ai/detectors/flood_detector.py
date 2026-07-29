import logging


logger = logging.getLogger("uvicorn.error")


class FloodDetector:

    """
    Initial flood detection layer.

    Later this will be replaced with:
    - segmentation model
    - water-level estimation
    - satellite/weather integration
    """

    WATER_CLASSES = {
        "water",
        "flood",
        "river",
    }


    @classmethod
    def evaluate(cls, detections):

        for detection in detections:

            label = detection.class_name.lower()

            if (
                label in cls.WATER_CLASSES
                and detection.confidence >= 0.60
            ):

                logger.info(
                    "🌊 Flood condition detected confidence=%.2f",
                    detection.confidence
                )

                return {
                    "incident_type": "flood",
                    "severity": "critical",
                    "confidence": detection.confidence,
                }


        return None