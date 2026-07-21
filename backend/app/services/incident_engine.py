from app.ai.emergency_labels import EMERGENCY_LABELS
from app.ai.models import Detection
from app.models.enums import Severity
from app.services.severity import SeverityEngine


class IncidentEngine:

    @staticmethod
    def evaluate(detection: Detection):

        if detection.label not in EMERGENCY_LABELS:
            return None

        severity = SeverityEngine.calculate(detection)

        return {
            "type": detection.label,
            "severity": severity,
            "confidence": detection.confidence,
            "camera_id": detection.camera_id,
        }