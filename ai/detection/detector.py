from ultralytics import YOLO


class Detector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        return self.model(frame)