from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.db.database import Base


class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True)

    incident_id = Column(
        Integer,
        ForeignKey("incidents.id"),
        nullable=False,
    )

    agency = Column(String(50), nullable=False)

    contact = Column(String(150), nullable=False)

    status = Column(
        String(30),
        default="pending",
    )

    sent_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    acknowledged_at = Column(DateTime(timezone=True))