import cv2
import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from anyio import to_thread
from app.services.detection_service import DetectionService

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

CAMERA_SOURCE = 0

# FIX: Added camera_id as a parameter to this worker function
def process_frame_ai(frame, camera_id):
    # FIX: Pass the camera_id right here into the DetectionService
    annotated_frame, incident = DetectionService.process(frame, camera_id=camera_id)

    # We'll send incidents to the IncidentManager in the next step.

    return annotated_frame

async def generate_frames():
    # cv2.VideoCapture works fine here, but keep CAP_DSHOW for rapid Windows camera hooks
    camera = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)

    if not camera.isOpened():
        logger.error("❌ Failed to bind to video capture device.")
        return

    logger.info("🚀 Camera linked successfully. Streaming active channels...")

    try:
        while True:
            # Read is a blocking I/O call; run off-thread to avoid loop lag
            success, frame = await to_thread.run_sync(camera.read)
            if not success:
                logger.warning("⚠️ Frame skip caught or device dropped stream sync.")
                break

            # FIX: Pass CAMERA_SOURCE as the secondary argument to the worker pool
            frame = await to_thread.run_sync(process_frame_ai, frame, CAMERA_SOURCE)

            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
    finally:
        camera.release()
        logger.info("🔒 Hardware resources completely released.")


@router.get("/stream")
async def stream_camera():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )