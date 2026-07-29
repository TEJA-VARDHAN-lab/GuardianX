from ultralytics import YOLO


model = YOLO(
    "models/yolo11s.pt"
)


print("GuardianX YOLO11s Ready")