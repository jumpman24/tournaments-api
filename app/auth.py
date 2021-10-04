from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from .settings import settings


pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(username: str):
    data = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(days=2),
    }
    return jwt.encode(data, settings.secret_key, jwt.ALGORITHMS.HS256)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, jwt.ALGORITHMS.HS256).get("sub")
    except JWTError:
        pass
