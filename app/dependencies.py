from fastapi import Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .managers import DatabaseManager


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_db_manager(session: Session = Depends(get_db)) -> DatabaseManager:
    return DatabaseManager(session)
