from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import UserPlanModel
from .schemas import UserPlanInput, UserPlanOutput


router = APIRouter(
    prefix="/user_plan",
    tags=["user_plan"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/", dependencies=[Depends(get_current_user)])
async def post(user: UserPlanInput):
    return UserPlanModel.create_plan(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
async def put(user: UserPlanInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return UserPlanModel.get_plans(user_id)
