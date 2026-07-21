from app.ai.models import Detection
from app.models.enums import Severity


class SeverityEngine:

    @staticmethod
    def calculate(detection: Detection) -> Severity:

        if detection.confidence > 0.95:
            return Severity.CRITICAL

        if detection.confidence > 0.85:
            return Severity.HIGH

        if detection.confidence > 0.70:
            return Severity.MEDIUM

        return Severity.LOW