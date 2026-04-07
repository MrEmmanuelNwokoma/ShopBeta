from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_favorite_service
from src.schemas.favorite_schema import CreateFavorites
from src.models.user import User
from src.services.favorite_services import FavoriteService


favorite_router = APIRouter(prefix="/api/v1/favorites", tags=["Favorite"])


@favorite_router.post("/")
async def create_favorite(
    favorite_data: CreateFavorites,
    user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service)
):
    
    response = await favorite_service.create_favorite(favorite_data, user_id = user.id)
    return response

