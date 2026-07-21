import cv2

from ai.camera.camera_service import CameraService
from ai.detection.detector import Detector


def run():

    camera = CameraService(0)

    detector = Detector()

    for frame in camera.frames():

        results = detector.detect(frame)

        annotated = results[0].plot()

        cv2.imshow("GuardianX", annotated)

        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()