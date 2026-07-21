from sqlalchemy import Column, Integer, Float, String

from app.db.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    stream_url = Column(String(500))

    location = Column(String(200))

    latitude = Column(Float)

    longitude = Column(Float)

    status = Column(String(30), default="offline")