import re

from pydantic import BaseModel, ConstrainedStr


class UsernameStr(ConstrainedStr):
    strip_whitespace = True
    to_lower = True
    min_length = 3
    max_length = 20
    regex = re.compile(r"^[a-zA-Z0-9]+([_.-][a-zA-Z0-9]+)*$")


class FullNameStr(ConstrainedStr):
    strip_whitespace = True
    min_length = 3
    max_length = 255


class UserCreateSchema(BaseModel):
    username: UsernameStr
    full_name: FullNameStr
    password: str


class UserSchema(BaseModel):
    id: int
    username: UsernameStr
    full_name: FullNameStr

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
