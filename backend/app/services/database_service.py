from sqlalchemy.orm import Session

from app.db.database import SessionLocal


class DatabaseService:
    """
    Provides short-lived database sessions for background services.
    """

    @staticmethod
    def session() -> Session:
        return SessionLocal()