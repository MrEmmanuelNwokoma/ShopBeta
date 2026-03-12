from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.product import Product



class ProductRepository(BaseRepository[Product]):
    "Product repository"
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
    
    async def get_brand(self, brand: str):
        result = await self.session.execute(select(self.model).where(self.model.brand == brand))
        return result.scalars().all()
    