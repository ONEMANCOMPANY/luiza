import datetime
from pydantic import BaseModel
from typing import Union


class UserInput(BaseModel):
    name: str
    surname: str
    phone: str
    mail: str
    cpf_cnpj: str
    user_type: str
    user_since: str
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserOutput(BaseModel):
    name: str
    surname: str
    phone: str
    mail: str
    user_type: str
    user_since: datetime.date
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserInDB(UserInput):
    password: str

class AuthUserToken(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: list


class TokenData(BaseModel):
    username: Union[str, None] = None
