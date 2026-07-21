import cv2

from app.ai.detector import GuardianDetector


class CameraStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.detector = GuardianDetector()

    def generate(self):
        while True:
            success, frame = self.cap.read()

            if not success:
                break

            annotated = self.detector.detect(frame)

            _, buffer = cv2.imencode(".jpg", annotated)

            frame_bytes = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )