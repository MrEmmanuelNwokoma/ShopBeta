from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_category_service
from src.services.category_services import CategoryService


category_router = APIRouter(prefix="/api/categories", tags=["Category"])

@category_router.get("/")
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service)
):
    response = await category_service.get_categories()
    return response

