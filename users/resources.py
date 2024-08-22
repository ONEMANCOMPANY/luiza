from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import UserModel
from .schemas import UserInput, UserOutput


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/")
async def post(user: UserInput):
    return UserModel.create_user(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def put(user: UserInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return UserModel.get_user(user_id)
