from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class Detection:
    class_name: str
    confidence: float
    source: str = "object"


class DetectionEngine:
    """
    Converts multiple AI model outputs into unified Detection objects.
    """

    MODEL_SOURCES = {
        0: "object_model",
        1: "fire_model",
        2: "weapon_model",
    }

    @staticmethod
    def parse(
        results: Any,
        source_name: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Detection]:
        detections: List[Detection] = []

        if not results:
            return detections

        # Ensure results is iterable (e.g., if a single result object is passed)
        if not isinstance(results, (list, tuple)):
            results_list = [results]
        else:
            results_list = results

        for index, result in enumerate(results_list):
            if not result or not hasattr(result, "boxes") or result.boxes is None:
                continue

            # Use explicitly passed source_name first; fallback to map index or unknown
            source = source_name or DetectionEngine.MODEL_SOURCES.get(
                index, "unknown_model"
            )

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Safely retrieve class name
                if hasattr(result, "names") and isinstance(result.names, dict):
                    class_name = result.names.get(class_id, f"class_{class_id}").lower()
                else:
                    class_name = f"class_{class_id}"

                detections.append(
                    Detection(
                        class_name=class_name,
                        confidence=confidence,
                        source=source,
                    )
                )

        return detections