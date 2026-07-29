import logging


logger = logging.getLogger("uvicorn.error")


class AlertMessageService:


    ACTION_MAP = {

        "fire":
            "Dispatch fire response team immediately. Evacuate nearby people.",

        "smoke":
            "Verify smoke source and deploy fire response unit.",

        "accident":
            "Dispatch police and ambulance. Provide medical assistance immediately.",

        "weapon":
            "Dispatch police unit. Treat location as high-risk.",

        "flood":
            "Activate disaster response team. Move civilians to safer areas.",

        "landslide":
            "Deploy disaster response team. Check road blockage and trapped civilians.",

    }


    @staticmethod
    def generate(
        incident,
        camera=None
    ):

        location = "Unknown"

        coordinates = "Unavailable"

        map_link = "Unavailable"


        if camera:

            location = camera.location_name

            coordinates = (
                f"{camera.latitude}, "
                f"{camera.longitude}"
            )

            map_link = (
                "https://maps.google.com/?q="
                f"{camera.latitude},{camera.longitude}"
            )


        incident_type = (
            incident.incident_type.lower()
        )


        action = AlertMessageService.ACTION_MAP.get(
            incident_type,
            "Assess situation and deploy appropriate emergency response."
        )


        snapshot_status = (
            f"Available: {incident.snapshot}"
            if incident.snapshot
            else "Not available"
        )


        message = f"""
🚨 GUARDIANX EMERGENCY ALERT 🚨


INCIDENT:
{incident_type.upper()}


SEVERITY:
{incident.severity.upper()}


AI CONFIDENCE:
{incident.confidence * 100:.1f}%


CAMERA:
ID {incident.camera_id}


LOCATION:
{location}


GPS:
{coordinates}


MAP:
{map_link}


RECOMMENDED ACTION:
{action}


SNAPSHOT:
{snapshot_status}


STATUS:
{incident.status.upper()}


Generated automatically by GuardianX AI Emergency Response System.
"""


        logger.info(
            "📢 Emergency message generated"
        )


        return message.strip()