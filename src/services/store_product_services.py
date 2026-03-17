from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFound, PermissionDenied
from src.enums.enums import UserRole
from src.schemas.store_product import CreateStoreProduct, ReadStoreProduct
from src.schemas.price_history_schema import CreatePriceHistory
from src.models.store_product import StoreProduct
from src.models.user import User


class StoreProductService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    async def add_product_to_store(self, current_user: User, store_product_data: CreateStoreProduct):
        store_id = store_product_data.store_id
        product_id = store_product_data.product_id
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            store = await self.uow_factory.store_repo.get_by_id(store_id)
            if not store:
                raise EntityNotFound(
                    message="Store not found",
                    details={
                        "recommendation": "Pass the correct store id"
                    }
                )
            product = await self.uow_factory.product_repo.get_by_id(product_id)
            if not product:
                raise EntityNotFound(
                    message="Product not found",
                    details={
                        "recommendation": "Pass the correct store id"
                    }
                )
            store_product = await self.uow_factory.store_product_repo.get_store_product(store_id, product_id)
            if store_product:
                raise EntityNotFound(
                    message="Store Product already exist in database",
                    details={
                        "recommendation": "Pass the correct store id and product_id."
                    }
                )
            data = store_product_data.model_dump()
            store_product = StoreProduct(**data)
            new_store_product = await self.uow_factory.store_product_repo.create(store_product)
            price_history_data = CreatePriceHistory.from_store_product(new_store_product)
            await self.uow_factory.price_history_repo.create_price_history(price_history_data)
        
            return ReadStoreProduct.model_validate(new_store_product)
    
    async def get_store_product(self, store_product_id: str):
        store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
        return store_product
    
    
    