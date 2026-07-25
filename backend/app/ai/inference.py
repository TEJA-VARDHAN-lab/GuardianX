import logging
import cv2

from ultralytics import YOLO

logger = logging.getLogger("uvicorn.error")


class InferenceEngine:

    object_model = YOLO("yolov8n.pt")
    fire_model = YOLO("models/fire_smoke.pt")

    @classmethod
    def detect(cls, frame, debug: bool = False):

        if frame is None:
            logger.error("❌ Empty frame received by inference engine")
            return [], []

        # Temporary debug frame capture
        if debug:
            cv2.imwrite(
                "debug_fire_frame_latest.jpg",
                frame
            )
            logger.info(
                "📸 Debug frame saved: debug_fire_frame.jpg"
            )

        # General object detection
        object_results = cls.object_model(
            frame,
            verbose=False,
        )

        # Fire / Smoke detection
        fire_results = cls.fire_model(
            frame,
            imgsz=640,
            conf=0.10,
            verbose=False,
        )

        # Raw fire model logging
        for result in fire_results:
            if result.boxes is not None:

                logger.info(
                    "🔥 Fire model boxes: %s",
                    len(result.boxes)
                )

                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names.get(
                        class_id,
                        f"class_{class_id}"
                    )

                    confidence = float(box.conf[0])

                    logger.info(
                        "🔥 RAW FIRE MODEL => %s %.2f",
                        class_name,
                        confidence,
                    )

        logger.info(
            "🧠 Models executed | objects=%s fire=%s",
            len(object_results),
            len(fire_results),
        )

        return object_results, fire_results