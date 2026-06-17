from datetime import datetime, timezone
from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.price_alert_schema import PriceAlertSchema, ReadPriceAlert
from src.core.exceptions import EntityNotFound, EntityAlreadyExist
from src.events.notification_event import NotificationCreatedEvent
from src.enums.enums import NotificationType
from src.schemas.notification import CreateNotification
from src.integrations.firebase import firebase_client


class PriceAlertService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory
        
    async def create_price_alert(self, price_alert_data: PriceAlertSchema, user_id: str):
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
            price_alert = await self.uow_factory.price_alert_repo.get_user_price_alert(price_alert_data, user_id)
            if price_alert:
                raise EntityAlreadyExist(
                    message="Price alert already exist",
                    details={
                        "recommendation": "Pass the correct price alert details"
                    }
                )
            
            new_price_alert = await self.uow_factory.price_alert_repo.create_price_alert(price_alert_data, user_id)
            store = await self.uow_factory.store_repo.get_by_id(store_product.store_id)
            product = await self.uow_factory.product_repo.get_by_id(store_product.product_id)
            
            return ReadPriceAlert(
                id=new_price_alert.id,
                store_product_id=store_product_id,
                product_name=product.name,
                store_name=store.name,
                target_price=new_price_alert.target_price
            )
        
    async def monitor_alert(self, store_product_id: str):

        store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
        
        if not store_product:
            raise EntityNotFound(
                message="Store product not found",
                details={
                    "recommendations": "Pass the correct store_product id"
                }
            )
        
        alerts = await self.uow_factory.price_alert_repo.get_untriggered_alerts(store_product_id)
        if not alerts:
            return 
        
        triggered_alerts = []

        for alert in alerts:
            if store_product.price <= alert.target_price:
                alert.is_active = False
                alert.is_triggered = True
                alert.is_triggered_at = datetime.now(timezone.utc)
                triggered_alerts.append(alert)
                await self.uow_factory.collect_event(NotificationCreatedEvent(
                    data=CreateNotification(
                        title="Price alert triggered",
                            message=f"Price has dropped to {store_product.price}, your target was {alert.target_price}",
                        notification_type=NotificationType.ALERT_TRIGGERED,
                        resource_id=store_product.id
                    ),
                    recipient_id=alert.user_id  
                ))
        if not triggered_alerts:
            return None
        print(triggered_alerts)
        # for triggered_alert in triggered_alerts:
        #     devices = await self.uow_factory.device_token_repo.get_user_devices(triggered_alert.user_id)
        #     for device in devices:
        #         device_token = device.token
        #         firebase_client.send_notification(
        #             token=device_token,
        #             title="Price Alert triggered",
        #             body=f"Price has dropped to {store_product.price}, your target was {triggered_alert.target_price}",
        #             data={
        #                 "store_product_id": store_product_id
        #             }
        #         )    

        return triggered_alerts
            