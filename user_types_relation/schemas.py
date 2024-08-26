import datetime
from pydantic import BaseModel
from typing import Union


class UserTypeInput(BaseModel):
    type_id: int
    user_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserTypeOutput(BaseModel):
    relation_id: int
    type_id: int
    user_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
