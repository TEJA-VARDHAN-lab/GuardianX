from ultralytics import YOLO
import cv2


model = YOLO("models/fire_smoke.pt")

image = cv2.imread("test_fire.jpg")

results = model(
    image,
    imgsz=640,
    conf=0.10
)

for result in results:
    print("Classes:", result.names)
    print("Boxes:", len(result.boxes))

    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        print(
            "Detected:",
            result.names[cls],
            conf
        )