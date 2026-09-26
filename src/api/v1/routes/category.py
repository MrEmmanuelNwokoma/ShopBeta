from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_category_service
from src.services.category_services import CategoryService
from src.schemas.category import ReadCategory, CreateCategory
from src.schemas.response_schema import ResponseWrapper
from src.schemas.product_schema import ReadProduct


category_router = APIRouter(prefix="/api/v1/categories", tags=["Category"])

@category_router.get("/", response_model=ResponseWrapper[list[ReadCategory]])
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service)
):
    response = await category_service.get_categories()
    return response

@category_router.get("/{id}/products", response_model=ResponseWrapper[list[ReadProduct]])
async def get_category_products(
    id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    response = await category_service.get_category_products(id)
    
    return response

