from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import IncidentService
from app.services.incident_workflow import can_transition

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])


class StatusUpdate(BaseModel):
    status: str


@router.get("", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)):
    return IncidentService.list_incidents(db)


@router.post("", response_model=IncidentResponse)
async def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
):
    return await IncidentService.create_incident(db, incident)


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
):
    incident = IncidentService.get_incident(db, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident record not found in system database.")

    if not can_transition(incident.status, payload.status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid incident transition: {incident.status} → {payload.status}",
        )

    return await IncidentService.update_status(db, incident_id, payload.status)