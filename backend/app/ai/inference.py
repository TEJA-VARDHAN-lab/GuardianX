from ultralytics import YOLO


class InferenceEngine:
    # Initialize both specialized model networks
    general_model = YOLO("yolov8n.pt")
    fire_model = YOLO("models/fire_smoke.pt")
    
    @classmethod
    def detect(cls, frame):
        """
        Runs the frame through both the general tracking model and the 
        custom fire/smoke model, combining the output arrays.
        """
        # 1. Evaluate general objects (people, vehicles, backpacks)
        general_results = cls.general_model(
            frame,
            conf=0.35,
            verbose=False,
        )

        # 2. Evaluate environmental hazard objects (fire, smoke)
        fire_results = cls.fire_model(
            frame,
            conf=0.15,
            verbose=False,
        )

        # 3. Combine results into a single flat list so DetectionService 
        # can iterate over or plot them seamlessly.
        combined_results = []
        if general_results:
            combined_results.extend(general_results)
        if fire_results:
            combined_results.extend(fire_results)

        return combined_results