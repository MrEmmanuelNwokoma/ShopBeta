from fastapi import APIRouter, Depends
from decimal import Decimal
from src.api.v1.dependencies import get_store_product_service
from src.services.store_product_services import StoreProductService
from src.schemas.response_schema import ResponseWrapper



store_product_router = APIRouter(prefix="/api/v1/store_products")

# @store_product_router.get("/products/{product_id}/compare_prices", response_model=list[ResponseWrapper])
# async def compare_prices(
#     product_id: str,
#     store_product_service: StoreProductService = Depends(get_store_product_service)
# ):
#     response = await store_product_service.compare_prices(product_id)
#     return response


@store_product_router.patch("/{store_product_id}/update_price")
async def update_store_product_prices(
    store_product_id: str,
    target_price: Decimal,
    store_product_service: StoreProductService = Depends(get_store_product_service)
):
    response = await store_product_service.update_product_price(store_product_ids=[store_product_id], target_price=target_price)
    return response