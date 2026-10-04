from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.favorites import Favorite
from src.models.store_product import StoreProduct
from src.schemas.favorite_schema import CreateFavorites



class FavoriteRepository(BaseRepository[Favorite]):
    def __init__(self, session: AsyncSession):
        super().__init__(Favorite, session)
    
    async def create_favorites(self, favorites_data: CreateFavorites, user_id: str):
        data = favorites_data.model_dump()
        data["user_id"] = user_id
        favorite = Favorite(**data)
        new_favorite = await self.create(favorite)
        return new_favorite
    
    async def get_user_favorites(self, user_id: str):
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                joinedload(self.model.store_product).joinedload(StoreProduct.store),
                joinedload(self.model.store_product).selectinload(StoreProduct.store_product_images),
            )
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_store_product_id(self, store_product_id: str):
        stmt = select(self.model).where(self.model.store_product_id == store_product_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()