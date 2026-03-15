from fastapi import APIRouter, Depends
from src.schemas.store_product import CreateStoreProduct
from src.api.v1.dependencies import get_store_product_service
from src.services.store_product_services import StoreProductService


store_product_router = APIRouter(prefix="/api/v1/store_products", tags=["Store Product"])

@store_product_router.post("/")
async def add_product_to_store(
    store_product_data: CreateStoreProduct,
    store_product_service: StoreProductService = Depends(get_store_product_service)
):
    response = await store_product_service.add_product_to_store(store_product_data)
    return response

