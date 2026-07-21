from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.incident import Incident


class DashboardService:

    @staticmethod
    def stats(db: Session):
        """
        Calculates real-time metrics for the GuardianX analytical dashboards.
        """
        # 1. Fetch all aggregate statistics across data tables
        stats_summary = db.query(
            func.count(case((Camera.status == "online", 1))).label("cameras_online")
        ).first()

        incident_summary = db.query(
            func.count(case((Incident.status != "resolved", 1))).label("active"),
            func.count(case((Incident.incident_type.in_([
                "fire", "fire_detected", "smoke", "smoke_detected"
            ]), 1))).label("fire"),
            func.count(case((Incident.severity == "critical", 1))).label("critical")
        ).first()

        # 🚀 FIX: Indented the debug block back into the method execution path
        print("===== DASHBOARD =====")
        print("Active  :", incident_summary.active if incident_summary else 0)
        print("Fire    :", incident_summary.fire if incident_summary else 0)
        print("Critical:", incident_summary.critical if incident_summary else 0)
        print("=====================")

        # 2. Extract values cleanly with fallback protection if tables are completely empty
        return {
            "cameras_online": stats_summary.cameras_online if stats_summary and stats_summary.cameras_online is not None else 0,
            "active_incidents": incident_summary.active if incident_summary and incident_summary.active is not None else 0,
            "fire_alerts": incident_summary.fire if incident_summary and incident_summary.fire is not None else 0,
            "critical_incidents": incident_summary.critical if incident_summary and incident_summary.critical is not None else 0,
        }