from fastapi import APIRouter, Depends
from src.schemas.store_product import CreateStoreProduct
from src.api.v1.dependencies import get_store_product_service, get_current_user
from src.services.store_product_services import StoreProductService
from src.models.user import User
from src.enums.enums import UserRole
from src.core.exceptions import PermissionDenied


store_product_router = APIRouter(prefix="/api/v1/store_products", tags=["Store Product"])

@store_product_router.post("/")
async def add_product_to_store(
    store_product_data: CreateStoreProduct,
    store_product_service: StoreProductService = Depends(get_store_product_service),
    user: User = Depends(get_current_user)
):
    if user.role != UserRole.ADMIN:
        raise PermissionDenied(
            message="You are not permitted to add prduct to store",
            details={
                "recommendation": "Pass the correct admin id"
            }
        )
    response = await store_product_service.add_product_to_store(store_product_data, current_user=user)
    return response

