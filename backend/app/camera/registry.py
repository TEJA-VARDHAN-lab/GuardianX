from typing import Dict

from app.camera.worker import CameraWorker


class CameraRegistry:

    workers: Dict[int, CameraWorker] = {}


    @classmethod
    def add(
        cls,
        camera_id: int,
        source: str,
    ):

        worker = CameraWorker(
            camera_id,
            source,
        )

        cls.workers[camera_id] = worker

        worker.start()


    @classmethod
    def remove(
        cls,
        camera_id: int,
    ):

        worker = cls.workers.get(
            camera_id
        )

        if worker:

            worker.stop()

            del cls.workers[camera_id]


    @classmethod
    def get(
        cls,
        camera_id: int,
    ):

        return cls.workers.get(
            camera_id
        )