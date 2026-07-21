from pydantic import BaseModel, ConfigDict


class IncidentCreate(BaseModel):
    camera_id: int
    incident_type: str
    severity: str
    confidence: float


class IncidentResponse(IncidentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    snapshot: str | None = None
    summary: str | None = None