from sqlalchemy import Boolean, Column, Float, Integer, String
from app.db.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String(150), nullable=False)

    source = Column(String(500), nullable=False)

    status = Column(
        String(20),
        default="offline",
        nullable=False,
    )

    ai_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
    )