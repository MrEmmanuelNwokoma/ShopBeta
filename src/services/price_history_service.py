from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFound
from src.schemas.price_history_schema import CreatePriceHistory, ReadPriceHistory

class PriceHistoryService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    
    async def get_store_product_price_history(self, store_product_id: str):
        async with self.uow_factory:
            price_history = await self.uow_factory.price_history_repo.get_store_product_price_history(store_product_id)
        return ReadPriceHistory.model_validate(price_history)
