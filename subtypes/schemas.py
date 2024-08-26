import datetime
from pydantic import BaseModel
from typing import Union


class SubTypeInput(BaseModel):
    subtype_name: str
    type_id = int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class TypeOutput(BaseModel):
    subtype_id: int
    subtype_name: str
    type_id = int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
