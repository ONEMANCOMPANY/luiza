import datetime
from pydantic import BaseModel
from typing import Union


class UserPlanInput(BaseModel):
    user_id: int
    plan_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserPlanOutput(BaseModel):
    user_id: int
    plan_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
