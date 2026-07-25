from pydantic import BaseModel


class CameraCreate(BaseModel):
    name: str
    location: str
    latitude: float
    longitude: float
    location_name: str
    source: str


class CameraResponse(BaseModel):
    id: int
    name: str
    location: str
    latitude: float
    longitude: float
    location_name: str
    source: str
    status: str
    ai_enabled: bool

    class Config:
        from_attributes = True