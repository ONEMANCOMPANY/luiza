import datetime
from pydantic import BaseModel
from typing import Union


class PlanInput(BaseModel):
    plan_name: str
    description: str
    price: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class PlanOutput(BaseModel):
    plan_name: str
    description: str
    price: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
