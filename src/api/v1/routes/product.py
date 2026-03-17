from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_product_service, get_current_user
from src.services.product_services import ProductService
from src.models.user import User
from src.schemas.product_schema import CreateProduct, UpdateProduct


product_router= APIRouter(prefix="/api/v1/products", tags=["Product"])

@product_router.post("/")
async def create_product(
    product_data: CreateProduct,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.create_product(product_data)
    return response

@product_router.post("/bulk")
async def bulk_create_products(
    products_data: list[CreateProduct],
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.bulk_create_products(products_data)
    return response

@product_router.get("/products")
async def get_multiple_products(
    product_ids: list[str],
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_multiple_products(product_ids)
    return response


@product_router.get("/{product_id}")
async def get_single_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_single_product(product_id)
    return response

@product_router.get("/{category_id}/products")
async def get_product_by_category(
    category_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.get_products_by_category(category_id)
    return response




@product_router.patch("/{product_id}")
async def update_product(
    product_id: str,
    product_data: UpdateProduct,
    current_user: User = Depends(get_current_user),
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.update_product(current_user, product_id, product_data)
    return response
 
@product_router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.delete_product(product_id)
    return response

@product_router.delete("/")
async def bulk_delete_products(
    products_id: list[str],
    product_service: ProductService = Depends(get_product_service)
):
    response = await product_service.bulk_delete_products(products_id)
    return response
