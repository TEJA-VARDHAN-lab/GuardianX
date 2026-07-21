from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.db.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    camera_id = Column(Integer, ForeignKey("cameras.id"))

    incident_type = Column(String(50))

    severity = Column(String(30))

    confidence = Column(Float)

    status = Column(String(30), default="detected")

    snapshot = Column(String(500))

    summary = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())