from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import create_token, get_password_hash, verify_password
from ..dependencies import get_current_user, get_db_manager
from ..managers import DatabaseManager
from ..models import User
from ..schemas.auth import TokenSchema, UserCreateSchema, UserSchema


router = APIRouter(tags=["auth"])


@router.post("/sign-up", response_model=TokenSchema)
def sign_up(
    data: UserCreateSchema,
    db: DatabaseManager = Depends(get_db_manager),
):
    users = db.get_instances(User, [User.username == data.username])

    if users:
        raise HTTPException(400, f"User >>{data.username}<< already exists")

    data.password = get_password_hash(data.password)
    user = db.create_instance(User, data)

    token = create_token(user.id)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/sign-in", response_model=TokenSchema)
def sign_in(
    data: OAuth2PasswordRequestForm = Depends(),
    db: DatabaseManager = Depends(get_db_manager),
):
    if not (users := db.get_instances(User, [User.username == data.username])):
        raise HTTPException(401, "Unauthorized")

    user = users[0]
    if not verify_password(data.password, user.password):
        raise HTTPException(401, "Unauthorized")

    token = create_token(user.id)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/whoami", response_model=UserSchema)
def check_token(current_user: User = Depends(get_current_user)):
    return current_user
