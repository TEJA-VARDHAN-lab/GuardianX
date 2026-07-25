from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.database import Base


class Agency(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    agency_type = Column(String(30), nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    contact = Column(String(150), nullable=False)

    active = Column(Boolean, default=True)