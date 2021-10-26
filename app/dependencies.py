from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .auth import decode_token
from .database import SessionLocal
from .managers import DatabaseManager
from .models import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/sign-in")


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_db_manager(session: Session = Depends(get_db)) -> DatabaseManager:
    return DatabaseManager(session)


def get_current_user(
    token: str = Depends(oauth2_schema),
    db: DatabaseManager = Depends(get_db_manager),
) -> Optional[User]:
    if token:
        if user_id := decode_token(token):
            if user := db.get_instance(User, user_id):
                return user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)


def get_current_user_websocket(
    token: str = None,
    db: DatabaseManager = Depends(get_db_manager),
) -> Optional[User]:
    if token:
        if user_id := decode_token(token):
            return db.get_instance(User, user_id)
