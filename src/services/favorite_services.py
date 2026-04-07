from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.favorite_schema import CreateFavorites
from src.models.user import User
from src.core.exceptions import EntityNotFound

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
    