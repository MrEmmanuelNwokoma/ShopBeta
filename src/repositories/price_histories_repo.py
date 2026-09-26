from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.price_history import PriceHistory
from src.schemas.price_history_schema import CreatePriceHistory

class PriceHistoryRepository(BaseRepository[PriceHistory]):
    def __init__(self, session: AsyncSession):
        super().__init__(PriceHistory, session)
    
    async def create_price_history(self, price_history_data: CreatePriceHistory):
        data = price_history_data.model_dump()
        price_history = PriceHistory(**data)
        new_price_history = await self.create(price_history)
        return new_price_history
    
    async def get_store_product_price_history(self, store_product_id: str):
        stmt = select(self.model).where(self.model.store_product_id == store_product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def bulk_create_price_history(
    self, payloads: list[CreatePriceHistory]
) -> list[PriceHistory]:
        
        if not payloads:
            return []

        records = [
            PriceHistory(
                store_product_id=p.store_product_id,
                price=p.price,
            )
            for p in payloads
        ]
        await self.bulk_create(records)
      
        return records