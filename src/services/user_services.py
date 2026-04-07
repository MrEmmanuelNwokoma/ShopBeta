from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.user_schema import ReadUser, UpdateUser
from src.schemas.price_alert_schema import ReadPriceAlert
from src.enums.enums import UserRole
from src.core.exceptions import PermissionDenied, EntityNotFound
from src.models.user import User



class UserService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
      

    async def update_user(self, user_data: UpdateUser, user_id: str, current_user: User):
        data = user_data.model_dump()
        async with self.uow_factory:
            user = await self.uow_factory.user_repo.get_by_id(user_id)
            if not user:
                raise EntityNotFound(
                    message="User not found",
                    details={
                        "recommendation": "Make sure you pass the correct user id"
                    }
                )
            if current_user.role != UserRole.ADMIN or current_user.id != user_id:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            await self.uow_factory.user_repo.update(user_id, data)
            return user_data
    
    async def get_user_price_alerts(self, user_id: str):
        async with self.uow_factory:

            price_alerts = await self.uow_factory.price_alert_repo.get_user_price_alerts(user_id)
            if not price_alerts:
                raise EntityNotFound(
                    message="User price alert not found",
                    details={
                        "recommendation": "Pass the correct user_id"
                    }
                )
            result = []
            for price_alert in price_alerts:
                store_product = await self.uow_factory.store_product_repo.get_by_id(price_alert.store_product_id)
                store = await self.uow_factory.store_repo.get_by_id(store_product.store_id)
                product = await self.uow_factory.product_repo.get_by_id(store_product.product_id)

                store_name = store.name
                product_name = product.name
                result.append(ReadPriceAlert(
                    product_name=product_name,
                    store_name=store_name,
                    target_price=price_alert.target_price
                ))
            return result
    
    async def get_user_favorites(self, user_id: str):
        async with self.uow_factory:
            user_favorites = await self.uow_factory.favorite_repo.get_user_favorites(user_id)
            return user_favorites
    
    