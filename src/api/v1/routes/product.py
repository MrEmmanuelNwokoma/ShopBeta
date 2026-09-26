from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_product_service
from src.services.product_services import ProductService
from src.schemas.product_schema import ReadProduct
from src.schemas.response_schema import ResponseWrapper
from src.schemas.store_product import ReadStoreProduct



product_router = APIRouter(prefix="/api/v1/products")


@product_router.get("/batch", response_model=ResponseWrapper[list[ReadProduct]])
async def get_multiple_products(
    product_ids: list[str],
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_multiple_products(product_ids)
    return response




@product_router.get("/", response_model=ResponseWrapper[list[ReadProduct]])
async def get_all_products(
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_all_products()
    return response

@product_router.get("/{product_id}", response_model=ResponseWrapper[ReadProduct])
async def get_single_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_single_product(product_id)
    return response


@product_router.get("/{product_id}/compare_stores", response_model=ResponseWrapper[ReadProduct])
async def compare_stores(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.compare_stores(product_id)
    return response
