from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import TypeModel
from .schemas import TypeInput, TypeOutput


router = APIRouter(
    prefix="/type",
    tags=["type"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/", dependencies=[Depends(get_current_user)])
async def post(user: TypeInput):
    return TypeModel.create_user_type(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
async def put(user: TypeInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return TypeModel.get_type(user_id)
