from datetime import datetime, timezone
from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.price_alert_schema import PriceAlertSchema, ReadPriceAlert
from src.core.exceptions import EntityNotFound, EntityAlreadyExist


class PriceAlertService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_price_alert(self, price_alert_data: PriceAlertSchema):
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
                id=new_price_alert.id,
                store_product_id=store_product_id,
                product_name=product.name,
                store_name=store.name,
                target_price=new_price_alert.target_price
            )
        
    async def monitor_alert(self, store_product_ids: list[str], current_price):
        async with self.uow_factory as uow:
            store_product = await uow.store_product_repo.get_by_id(store_product_ids)
            if not store_product:
                raise EntityNotFound(
                    message="Store product not found",
                    details={
                        "recommendations": "Pass the correct store_product id"
                    }
                )
            
            alerts = await uow.price_alert_repo.get_untriggered_alerts(store_product_ids)

            triggered_alerts = []

            for alert in alerts:
                if current_price <= alert.target_price:
                    alert.is_active = True
                    alert.is_triggered = True
                    alert.is_triggered_at = datetime.now(timezone.utc)
                    triggered_alerts.append(alert)
            
            return triggered_alerts
            