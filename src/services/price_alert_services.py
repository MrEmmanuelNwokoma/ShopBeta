from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.price_alert_schema import PriceAlert, ReadPriceAlert
from src.core.exceptions import EntityNotFound, EntityAlreadyExist


class PriceAlertService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_price_alert(self, price_alert_data: PriceAlert):
        store_product_id = price_alert_data.store_product_id
        async with self.uow_factory:
            store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
            if not store_product:
                raise EntityNotFound(
                    message="Store product not found",
                    details={
                        "recommendations": "Pass the correct store_product id"
                    }
                )
            if price_alert_data.target_price <= 0:
                raise ValueError("Target price must be greater than 0")
            price_alert = await self.uow_factory.price_alert_repo.get_user_price_alert(price_alert_data)
            if price_alert:
                raise EntityAlreadyExist(
                    message="Price alert already exist",
                    details={
                        "recommendation": "Pass the correct price alert details"
                    }
                )
            new_price_alert = await self.uow_factory.price_alert_repo.create_price_alert(price_alert_data)
            store = await self.uow_factory.store_repo.get_by_id(store_product.store_id)
            product = await self.uow_factory.product_repo.get_by_id(store_product.product_id)
            
        return ReadPriceAlert(
            product_name=product.name,
            store_name=store.name,
            target_price=new_price_alert.target_price
        )