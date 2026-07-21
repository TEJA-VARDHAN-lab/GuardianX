import cv2


class CameraService:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)

    def frames(self):
        while True:
            success, frame = self.cap.read()

            if not success:
                break

            yield frame

    def release(self):
        self.cap.release()