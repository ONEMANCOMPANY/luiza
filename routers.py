from fastapi import APIRouter
from users.resources import router as users_router
from auth.resources import router as auth_router
from plans.resources import router as plans_router
from user_plan.resources import router as user_plan_router


# routes
router = APIRouter()
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(plans_router)
router.include_router(user_plan_router)
