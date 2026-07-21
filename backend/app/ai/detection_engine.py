from dataclasses import dataclass


@dataclass
class Detection:
    class_name: str
    confidence: float


class DetectionEngine:
    """
    Converts YOLO results into simplified Detection objects.
    """

    @staticmethod
    def parse(results) -> list[Detection]:
        detections: list[Detection] = []

        if not results:
            return detections

        result = results[0]

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]

            detections.append(
                Detection(
                    class_name=class_name,
                    confidence=confidence,
                )
            )

        return detections