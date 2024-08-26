import datetime
from pydantic import BaseModel
from typing import Union


class TypeInput(BaseModel):
    type_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class TypeOutput(BaseModel):
    type_id: int
    type_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
