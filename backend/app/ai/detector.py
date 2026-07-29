from ultralytics import YOLO


class GuardianDetector:
    def __init__(self):
        self.model = YOLO("models/yolo11s.pt")

    def detect(self, frame):
        results = self.model(frame)
        return results[0].plot()