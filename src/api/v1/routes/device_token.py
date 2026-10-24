import os
import sqlite3
import tempfile
from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from sqlalchemy.engine import make_url
from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_device_token_service
from src.schemas.device_token_schema import AddDeviceToken
from src.services.device_token import DeviceTokenService
from src.models.user import User
from src.enums.enums import UserRole
from src.core.pydantic_configuration import config
from src.


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


@device_token_router.get("/debug/db")
async def download_db(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403)
    src_path = make_url("sqlite+aiosqlite:///my_database.db").database
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    src, dst = sqlite3.connect(src_path), sqlite3.connect(tmp.name)
    src.backup(dst)  # consistent snapshot, includes recent writes
    dst.close()
    src.close()
    return FileResponse(
        tmp.name,
        filename="render_copy.db",
        background=BackgroundTask(os.remove, tmp.name),
    )