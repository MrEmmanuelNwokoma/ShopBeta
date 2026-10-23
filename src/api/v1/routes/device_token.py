from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_device_token_service
from src.schemas.device_token_schema import AddDeviceToken
from src.services.device_token import DeviceTokenService
from src.models.user import User


device_token_router = APIRouter(
    prefix="/api/v1/device_tokens", tags=["Device Tokens"]
)

@device_token_router.post("/")
async def add_device_token(
    device_data: AddDeviceToken,
    user: User = Depends(get_current_user),
    device_token_service: DeviceTokenService = Depends(get_device_token_service)
):
    response = await device_token_service.add_device_token(device_data, user.id)
    return response

@device_token_router.delete("/")
async def delete_device_tokens(
    tokens: list[str],
    device_token_service: DeviceTokenService = Depends(get_device_token_service)
):
    response = await device_token_service.delete_device_tokens(tokens)
    return response

@device_token_router.get("/")
async def get_user_devices(
    user: User = Depends(get_current_user),
    device_token_service: DeviceTokenService = Depends(get_device_token_service)
):
    response = await device_token_service.get_user_devices(user.id)
    return response