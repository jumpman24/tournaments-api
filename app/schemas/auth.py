import re

from pydantic import BaseModel, ConstrainedStr


def to_camel_case(snake_case: str) -> str:
    camel_case, *words = snake_case.split("_")
    for word in words:  # type: str
        camel_case += word.capitalize()
    return camel_case


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
        alias_generator = to_camel_case


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
