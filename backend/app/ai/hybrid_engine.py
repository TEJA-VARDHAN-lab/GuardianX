import logging

from app.ai.pipeline import VisionPipeline
from app.ai.detectors.fire_detector import FireDetector

logger = logging.getLogger("uvicorn.error")


class HybridAIEngine:

    @staticmethod
    def analyze(frame):
        """
        Main GuardianX intelligence layer.

        Always runs local AI.
        Cloud enhancement can be added later.
        """
        incidents = []

        # 1. Run specialized fire detection
        fire_results = FireDetector.detect(frame)
        if fire_results:
            incidents.extend(fire_results)

        # 2. Run general vision pipeline
        local_results = VisionPipeline.analyze(frame)

        for result in local_results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = result.names[class_id]

                incidents.append(
                    {
                        "type": label,
                        "confidence": confidence
                    }
                )

        logger.info(
            "AI Analysis completed: %s",
            incidents
        )

        return incidents