import logging
import torch
from ultralytics import YOLO
from app.ai.detectors.fire_detector import FireDetector
from app.ai.detectors.weapon_detector import WeaponDetector

logger = logging.getLogger("uvicorn.error")

# CPU thread tuning for multi-threaded inference performance
torch.set_num_threads(6)


class ModelManager:

    object_model = None
    fire_model = None
    weapon_model = None

    @classmethod
    def load_models(cls):
        """
        Loads and initializes all GuardianX AI vision models.
        """
        # Guard clause to prevent duplicate re-loads on server refreshes
        if cls.object_model and cls.fire_model and cls.weapon_model:
            logger.info("⚡ GuardianX AI models are already loaded in memory.")
            return

        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("🧠 Loading GuardianX AI models on device: [%s]...", device.upper())

        try:
            # Load specialized detector modules
            FireDetector.load()
            WeaponDetector.load()

            # Load YOLO model weights onto detected hardware
            cls.object_model = YOLO("models/yolo11s.pt").to(device)
            cls.fire_model = YOLO("models/fire_smoke.pt").to(device)
            cls.weapon_model = YOLO("models/weapon.pt").to(device)

            logger.info("✅ GuardianX AI models loaded successfully!")

        except Exception as e:
            logger.error("❌ Failed to load GuardianX AI models: %s", e)
            raise e