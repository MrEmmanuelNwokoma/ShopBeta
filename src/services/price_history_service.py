from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFound
from src.schemas.price_history_schema import CreatePriceHistory, ReadPriceHistory

class PriceHistoryService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    
    async def get_store_product_price_history(self, store_product_id: str):
        async with self.uow_factory:
            store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
            if not store_product:
                raise EntityNotFound(
                    message="Store product not found",
                    details={"recommendation": "Pass a valid store_product_id"}
                )
            price_history = await self.uow_factory.price_history_repo.get_store_product_price_history(store_product_id)
            if not price_history:
                return []
            return ReadPriceHistory.model_validate(price_history)