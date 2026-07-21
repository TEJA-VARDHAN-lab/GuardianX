from pydantic import BaseModel

class DashboardStats(BaseModel):
    cameras_online: int
    active_incidents: int
    fire_alerts: int
    critical_incidents: int