from fastapi import APIRouter, Depends
from src.models.store import Store
from src.models.user import User
from src.services.store_services import StoreService
from src.api.v1.dependencies import get_store_service, get_current_user
from src.schemas.store_schema import CreateStore, UpdateStore



store_router = APIRouter(prefix="/api/v1/stores", tags=["Stores"])

@store_router.post("/")
async def create_store(
    store_data: CreateStore,
    current_user: User = Depends(get_current_user),
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.create_store(current_user=current_user, store_data=store_data)
    return response


@store_router.get("/{store_id}")
async def get_single_store(
    store_id: str,
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.get_single_store(store_id)
    return response


@store_router.get("/stores")
async def get_all_stores(
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.get_all_stores()
    return response


@store_router.patch("/{store_id}")
async def update_store(
    store_id: str,
    store_data: UpdateStore,
    current_user: User = Depends(get_current_user),
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.update_store(current_user, store_id, store_data)
    return response

@store_router.delete("/{store_id}")
async def deactivate_store(
    store_id: str,
    current_user: User = Depends(get_current_user),
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.deactivate_store(current_user, store_id)
    return response
