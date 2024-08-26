from fastapi import APIRouter, status, Depends
from internal.dependencies import get_current_user
from .models import SubTypeModel
from .schemas import SubTypeInput, SubTypeOutput


router = APIRouter(
    prefix="/subtype",
    tags=["subtype"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.post("/", dependencies=[Depends(get_current_user)])
async def post(user: SubTypeInput):
    return SubTypeModel.create_user_subtype(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
async def put(user: SubTypeInput):
    ...


@router.get("/", dependencies=[Depends(get_current_user)])
async def get(user_id: int = None):
    return SubTypeModel.get_subtype(user_id)
