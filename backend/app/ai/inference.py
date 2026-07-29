import logging
import cv2
import os
from typing import Optional, Tuple, Any
from ultralytics import YOLO

logger = logging.getLogger("uvicorn.error")


class InferenceEngine:
    _initialized: bool = False
    object_model: Optional[YOLO] = None
    fire_model: Optional[YOLO] = None
    weapon_model: Optional[YOLO] = None

    @classmethod
    def initialize(cls) -> None:
        """Lazy-loads all YOLO model weights into memory on startup."""
        if cls._initialized:
            return

        logger.info("🚀 Initializing Inference Engine models...")

        # 1. Base Object Detection Model
        try:
            cls.object_model = YOLO("yolo11s.pt")
            logger.info("📦 Object model ('yolo11s.pt') loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load object model: {e}")

        # 2. Fire / Smoke Detection Model
        fire_model_path = "models/fire_smoke.pt"
        if os.path.exists(fire_model_path):
            try:
                cls.fire_model = YOLO(fire_model_path)
                logger.info(f"🔥 Fire model ('{fire_model_path}') loaded successfully.")
            except Exception as e:
                logger.error(f"❌ Error loading fire model: {e}")
        else:
            logger.warning(f"⚠️ Fire model path '{fire_model_path}' not found.")

        # 3. Weapon Detection Model
        # Checking primary and fallback paths
        weapon_paths = ["models/weapons/weapon_detector.pt", "models/weapon.pt"]
        weapon_path = next((p for p in weapon_paths if os.path.exists(p)), None)

        if weapon_path:
            try:
                cls.weapon_model = YOLO(weapon_path)
                logger.info(f"🔫 Weapon model ('{weapon_path}') loaded successfully.")
            except Exception as e:
                logger.error(f"❌ Error loading weapon model: {e}")
        else:
            logger.warning("🔫 No weapon model found — weapon detection disabled.")

        cls._initialized = True

    @classmethod
    def detect(cls, frame, debug: bool = False) -> Tuple[Any, Any, Any]:
        if not cls._initialized:
            cls.initialize()

        if frame is None:
            logger.error("❌ Empty frame received by inference engine")
            return [], [], []

        # Debug frame capture
        if debug:
            cv2.imwrite("debug_fire_frame_latest.jpg", frame)
            logger.info("📸 Debug frame saved: debug_fire_frame_latest.jpg")

        # 1. General Object Detection
        object_results = cls.object_model(frame, verbose=False) if cls.object_model else []

        # 2. Fire / Smoke Detection
        fire_results = (
            cls.fire_model(frame, imgsz=640, conf=0.10, verbose=False)
            if cls.fire_model
            else []
        )

        # 3. Weapon Detection
        weapon_results = (
            cls.weapon_model(frame, imgsz=640, conf=0.25, verbose=False)
            if cls.weapon_model
            else []
        )

        # Raw Fire Logging
        for result in fire_results:
            if hasattr(result, "boxes") and result.boxes is not None:
                logger.info("🔥 Fire model boxes detected: %s", len(result.boxes))

                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names.get(class_id, f"class_{class_id}")
                    confidence = float(box.conf[0])

                    logger.info("🔥 RAW FIRE MODEL => %s %.2f", class_name, confidence)

        # Telemetry Summary
        def get_count(res):
            if not res:
                return 0
            if isinstance(res, list) and len(res) > 0 and hasattr(res[0], "boxes"):
                return sum(len(r.boxes) for r in res if r.boxes is not None)
            return len(res)

        logger.info(
            "🧠 Models executed | objects=%s fire=%s weapons=%s",
            get_count(object_results),
            get_count(fire_results),
            get_count(weapon_results),
        )

        return object_results, fire_results, weapon_results