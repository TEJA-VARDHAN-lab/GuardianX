import logging

from app.db.database import SessionLocal
from app.models.incident import Incident
from app.models.camera import Camera


logger = logging.getLogger("uvicorn.error")


class SystemContextService:


    @staticmethod
    def get_context():

        db = SessionLocal()

        try:

            active_incidents = (
                db.query(Incident)
                .filter(
                    Incident.status != "resolved"
                )
                .count()
            )


            latest_incident = (
                db.query(Incident)
                .order_by(
                    Incident.created_at.desc()
                )
                .first()
            )


            if latest_incident:

                camera = (
                    db.query(Camera)
                    .filter(
                        Camera.id ==
                        latest_incident.camera_id
                    )
                    .first()
                )


                latest = {

                    "type":
                    latest_incident.incident_type,

                    "severity":
                    latest_incident.severity,

                    "confidence":
                    latest_incident.confidence,

                    "camera":
                    camera.name
                    if camera else "Unknown",

                    "location":
                    camera.location_name
                    if camera else "Unknown",

                }

            else:

                latest = None


            return {

                "active_incidents":
                active_incidents,

                "latest_incident":
                latest,

            }


        finally:

            db.close()