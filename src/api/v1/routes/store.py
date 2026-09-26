from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_store_service
from src.services.store_services import StoreService
from src.schemas.response_schema import ResponseWrapper




store_router = APIRouter(prefix="/api/v1/stores", tags=["Store"])

@store_router.delete("/{store_id}")
async def delete_store(
    store_id: str,
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.deactivate_store(store_id)
    return response

@store_router.put("/{store_id}/activate")
async def activate_store(
    store_id: str,
    store_service: StoreService = Depends(get_store_service)
):
    response = await store_service.activate_store(store_id)
    return response
