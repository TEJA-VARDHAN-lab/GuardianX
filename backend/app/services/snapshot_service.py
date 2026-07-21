import os
import cv2
import time

SNAPSHOT_DIR = "snapshots"


class SnapshotService:

    @staticmethod
    def save(frame, incident_type):
        """
        Saves the current video frame as a JPEG image inside the snapshot directory.
        """
        os.makedirs(
            SNAPSHOT_DIR,
            exist_ok=True
        )

        filename = (
            f"{incident_type}_"
            f"{int(time.time())}.jpg"
        )

        path = os.path.join(
            SNAPSHOT_DIR,
            filename
        )

        success = cv2.imwrite(path, frame)

        # 🚀 FIX: Safely indented inside the staticmethod block
        print(f"📸 Snapshot saved: {success} -> {path}")

        return path if success else None