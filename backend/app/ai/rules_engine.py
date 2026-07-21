from app.ai.detection_engine import Detection


class RulesEngine:

    @staticmethod
    def evaluate(detections: list[Detection]):

        for detection in detections:

            cls = detection.class_name.lower()

            # Fire
            if cls == "fire":
                return {
                    "incident_type": "fire",
                    "severity": "critical",
                    "confidence": detection.confidence,
                }

            # Smoke
            if cls == "smoke":
                return {
                    "incident_type": "smoke",
                    "severity": "high",
                    "confidence": detection.confidence,
                }

            # Person
            if cls == "person":
                return {
                    "incident_type": "person_detected",
                    "severity": "medium",
                    "confidence": detection.confidence,
                }

        return None