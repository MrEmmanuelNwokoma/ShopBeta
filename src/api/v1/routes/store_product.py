from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_store_product_service
from src.services.store_product_services import StoreProductService
from src.schemas.response_schema import ResponseWrapper



store_product_router = APIRouter(prefix="/api/v1/store_products")

@store_product_router.get("/products/{product_id}/compare_prices", response_model=list[ResponseWrapper])
async def compare_prices(
    product_id: str,
    store_product_service: StoreProductService = Depends(get_store_product_service)
):
    response = await store_product_service.compare_prices(product_id)
    return response