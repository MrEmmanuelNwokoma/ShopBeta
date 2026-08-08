from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.favorite_schema import CreateFavorites
from src.models.user import User
from src.core.exceptions import EntityNotFound, PermissionDenied

class FavoriteService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    async def create_favorite(self, favorite_data: CreateFavorites, user_id: str):
        async with self.uow_factory:
            user = await self.uow_factory.user_repo.get_by_id(user_id)
            if not user:
                raise EntityNotFound(
                    message="User not found",
                    details={
                        "recommendation": "Pass the correct user id"
                    }
                )
            store_product = await self.uow_factory.store_product_repo.get_by_id(favorite_data.store_product_id)
            if not store_product:
                raise EntityNotFound(
                    message="Store product not found",
                    details={
                        "recommendation": "Pass the correct store product id"
                    }
                ) 
            
            favorite = await self.uow_factory.favorite_repo.create_favorites(favorite_data, user_id)
            return favorite
        
        
    async def delete_favorites(self, favorite_id: str, user_id: str):
        async with self.uow_factory:
            favorite = await self.uow_factory.favorite_repo.get_by_id(favorite_id)
            if not favorite:
                raise EntityNotFound(
                    message="Favorite not found",
                    details={
                        "recommendation": "Pass the correct favorite id"
                    }
                )
            if favorite.user_id != user_id:
                raise PermissionDenied(
                    message="Permission denied",
                    details={
                        "recommendation": "You do not have the permission to delete favorite"
                    }
                )
            await self.uow_factory.favorite_repo.delete(favorite_id)
            return {
                "status": "success",
                "message": "Favorite deleted successfully"
            }