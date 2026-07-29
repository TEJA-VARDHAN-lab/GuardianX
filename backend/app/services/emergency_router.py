import logging

logger = logging.getLogger("uvicorn.error")


class EmergencyRouter:

    DEPARTMENT_MAP = {
        "fire": ["FIRE_DEPARTMENT"],
        "smoke": ["FIRE_DEPARTMENT"],
        "accident": ["POLICE", "AMBULANCE"],
        "weapon": ["POLICE"],
        "flood": ["DISASTER_RESPONSE"],
        "landslide": ["BSF", "DISASTER_RESPONSE"],
    }

    @classmethod
    def get_departments(cls, incident_type: str) -> list[str]:
        """Retrieves targeted emergency response departments by incident type."""
        if not incident_type:
            return []
        return cls.DEPARTMENT_MAP.get(incident_type.lower(), [])

    @classmethod
    def dispatch(
        cls,
        incident_type: str,
        severity: str,
        confidence: float,
        camera,
        snapshot=None,
    ) -> dict:
        """Constructs and logs an emergency alert message payload."""
        departments = cls.get_departments(incident_type)

        message = {
            "incident_type": incident_type,
            "severity": severity,
            "confidence": confidence,
            "camera_id": getattr(camera, "id", None),
            "location": getattr(camera, "location_name", "Unknown Location"),
            "latitude": getattr(camera, "latitude", None),
            "longitude": getattr(camera, "longitude", None),
            "departments": departments,
            "snapshot": snapshot,
        }

        logger.warning("🚨 EMERGENCY ALERT %s", message)

        return message