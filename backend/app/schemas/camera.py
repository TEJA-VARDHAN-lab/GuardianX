from pydantic import BaseModel, ConfigDict


class CameraCreate(BaseModel):
    name: str
    stream_url: str
    location: str
    latitude: float
    longitude: float


class CameraResponse(CameraCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str