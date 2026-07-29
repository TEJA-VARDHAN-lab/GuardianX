from ultralytics import YOLO
import logging
import os


logger = logging.getLogger("uvicorn.error")


class WeaponDetector:

    model = None

    MODEL_PATH = "models/weapon.pt"


    @classmethod
    def load(cls):

        if cls.model is not None:
            return


        if not os.path.exists(cls.MODEL_PATH):

            logger.warning(
                "🔫 Weapon model missing: %s",
                cls.MODEL_PATH
            )

            return


        cls.model = YOLO(
            cls.MODEL_PATH
        )


        logger.info(
            "🔫 Weapon detection model loaded"
        )


    @classmethod
    def predict(cls, frame):

        if cls.model is None:
            cls.load()


        if cls.model is None:
            return []


        return cls.model(
            frame,
            verbose=False
        )