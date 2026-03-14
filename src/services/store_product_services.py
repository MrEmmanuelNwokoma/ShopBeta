from src.unit_of_work.unit_of_work import UnitOfWork


class StoreProductService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    # async def add_product_to_store(self, store_id: str, )