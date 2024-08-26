from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import PlanModel
from .schemas import PlanInput, PlanOutput


router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/")
async def post(user: PlanInput):
    return PlanModel.create_plan(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def put(user: PlanInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return PlanModel.get_plans(user_id)
