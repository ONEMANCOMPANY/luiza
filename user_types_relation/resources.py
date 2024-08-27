from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import UserTypeRelationModel
from .schemas import UserTypeInput, UserTypeOutput


router = APIRouter(
    prefix="/user_type_relation",
    tags=["user_type_relation"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/", dependencies=[Depends(get_current_user)])
async def post(user: UserTypeInput):
    return UserTypeRelationModel.create_relation(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
async def put(user: UserTypeInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return UserTypeRelationModel.get_relation(user_id)
