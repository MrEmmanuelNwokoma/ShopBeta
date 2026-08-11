from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.store_product import StoreProduct
from src.repositories.base import BaseRepository

class StoreProductRepository(BaseRepository[StoreProduct]):
    def __init__(self, session: AsyncSession):
        super().__init__(StoreProduct, session)

    async def get_store_product(self, store_id: str, product_id: str):
        stmt = select(self.model).where(
            self.model.store_id == store_id,
            self.model.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_product_prices(self, product_id: str):
        stmt = select(self.model).where(self.model.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
