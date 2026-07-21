from pathlib import Path
from datetime import datetime

import cv2


class ImageService:

    SNAPSHOT_DIR = Path("snapshots")

    @classmethod
    def save_snapshot(cls, frame):
        cls.SNAPSHOT_DIR.mkdir(exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"

        filepath = cls.SNAPSHOT_DIR / filename

        cv2.imwrite(str(filepath), frame)

        return str(filepath)