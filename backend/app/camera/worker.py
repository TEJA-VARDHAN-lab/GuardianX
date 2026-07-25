import logging
import threading
import time
import cv2

from app.services.detection_service import DetectionService

logger = logging.getLogger("uvicorn.error")


class CameraWorker:

    def __init__(self, camera_id: int, source: str):
        self.camera_id = camera_id
        self.source = source

        self.running = False
        self.thread = None

        self.latest_frame = None

        self.fps = 0.0
        self.last_update = None

        self.status = "offline"
        self.last_frame_time = None
        self.frame_count = 0

    def start(self):
        if self.running:
            return

        self.running = True
        self.status = "starting"

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self.thread.start()

        logger.info(
            "📹 Camera %s worker started",
            self.camera_id,
        )

    def stop(self):
        self.running = False

        logger.info(
            "🛑 Camera %s worker stopped",
            self.camera_id,
        )

    def _run(self):
        # 1. Determine if source is an integer index (webcam) or file/stream path
        is_webcam = str(self.source).isdigit()
        camera_source = int(self.source) if is_webcam else self.source

        # 2. Use DSHOW only for Windows webcams; default backend for video files/RTSP
        if is_webcam:
            camera = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
        else:
            camera = cv2.VideoCapture(camera_source)

        if not camera.isOpened():
            self.status = "offline"
            logger.error("❌ Camera %s failed to open source: %s", self.camera_id, self.source)
            return

        self.status = "online"
        logger.info("🟢 Camera %s online", self.camera_id)

        previous = time.time()

        while self.running:
            success, frame = camera.read()

            if not success:
                # Avoid CPU pinning if feed stalls or loops video file
                time.sleep(0.01)
                continue

            # Run detection inference pipeline
            annotated, _ = DetectionService.process(
                frame,
                camera_id=self.camera_id,
            )

            self.latest_frame = annotated
            self.last_frame_time = time.time()
            self.frame_count += 1

            now = time.time()
            delta = now - previous

            # Prevent division by zero
            if delta > 0:
                self.fps = round(1 / delta, 2)

            previous = now
            self.last_update = now

        camera.release()
        self.status = "offline"

    def health(self):
        return {
            "camera_id": self.camera_id,
            "status": self.status,
            "fps": self.fps,
            "last_frame": self.last_frame_time,
            "running": self.running,
        }

    def get_jpeg(self):
        if self.latest_frame is None:
            return None

        success, buffer = cv2.imencode(".jpg", self.latest_frame)

        if not success:
            return None

        return buffer.tobytes()