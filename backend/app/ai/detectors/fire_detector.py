from ultralytics import YOLO
import logging
import os


logger = logging.getLogger("uvicorn.error")


class FireDetector:

    model = None


    MODEL_PATH = "models/fire_smoke.pt"


    @classmethod
    def load(cls):

        if cls.model is not None:
            return


        if not os.path.exists(cls.MODEL_PATH):

            logger.warning(
                "🔥 Fire model not found: %s",
                cls.MODEL_PATH
            )

            return


        cls.model = YOLO(
            cls.MODEL_PATH
        )


        logger.info(
            "🔥 Fire/Smoke detection model loaded"
        )


    @classmethod
    def detect(cls, frame):

        if cls.model is None:
            cls.load()


        if cls.model is None:
            return []


        results = cls.model(
            frame,
            verbose=False
        )


        detections = []


        for result in results:

            if result.boxes is None:
                continue


            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )


                class_id = int(
                    box.cls[0]
                )


                label = result.names[class_id]


                detections.append(
                    {
                        "type": label,
                        "confidence": confidence,
                    }
                )


        return detections