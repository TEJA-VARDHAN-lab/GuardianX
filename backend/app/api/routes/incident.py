from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])


# Quick schema to enforce validation on incoming patch payload structures
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
    payload: StatusUpdate,  # Captures validation values natively from JSON body payload
    db: Session = Depends(get_db),
):
    # Extracts the string from our data transfer validation layer
    incident = IncidentService.update_status(
        db,
        incident_id,
        payload.status,
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident record not found in system database.",
        )

    return incident