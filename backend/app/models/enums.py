from enum import Enum


class IncidentStatus(str, Enum):
    DETECTED = "detected"
    VERIFIED = "verified"
    RESOLVED = "resolved"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"