from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    camera_id: int
    timestamp: datetime