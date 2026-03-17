from fastapi import APIRouter, Depends
from src.models.user import User
from src.api.v1.dependencies import get_current_user, get_user_service
from src.services.user_services import UserService
from src.schemas.user_schema import UpdateUser


user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@user_router.get("/me/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@user_router.patch("")
async def update_user_profile(
    user_data: UpdateUser,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    response = await user_service.update_user(user_data, user_id=current_user.id)
    return response

@user_router.get("/me/price-alerts")
async def get_user_price_alerts(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    response = await user_service.get_user_price_alerts(user_id=user.id)
    return response
    
    