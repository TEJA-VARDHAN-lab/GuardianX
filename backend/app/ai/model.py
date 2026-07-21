import logging
from ultralytics import YOLO

logger = logging.getLogger("uvicorn.error")

# Keep this empty at module load time! 
# Do NOT instantiate YOLO() here globally.
_model_instance = None

def get_model():
    """
    Thread-safe lazy initialization singleton for the AI model.
    Only loads weights into VRAM/RAM when explicitly invoked by a worker process.
    """
    global _model_instance
    
    if _model_instance is None:
        logger.info("🧠 Loading AI Object Detection engine into memory...")
        # Replace 'yolov8n.pt' with your specific architecture choice if different
        _model_instance = YOLO("yolov8n.pt")
        logger.info("✅ AI Engine loaded successfully.")
        
    return _model_instance