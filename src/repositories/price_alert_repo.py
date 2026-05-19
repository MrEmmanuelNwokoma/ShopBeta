from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.price_alert import PriceAlert
from src.schemas.price_alert_schema import PriceAlertSchema


class PriceAlertRepository(BaseRepository[PriceAlert]):
    def __init__(self, session: AsyncSession):
        super().__init__(PriceAlert, session)

    async def create_price_alert(self, price_alert_data: PriceAlertSchema, user_id: str):
        data = price_alert_data.model_dump()
        price__alert = PriceAlert(**data, user_id=user_id)
        new_price_alert = await self.create(price__alert)
        return new_price_alert
    
    async def get_user_price_alerts(self, user_id: str):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_user_price_alert(self, price_alert_data: PriceAlert, user_id: str):
        stmt = select(self.model).where(
            self.model.target_price == price_alert_data.target_price,
            self.model.store_product_id == price_alert_data.store_product_id,
            self.model.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_untriggered_alerts(self, store_product_id: str):
        stmt = select(self.model).where(
            self.model.store_product_id ==store_product_id,
            self.model.is_triggered == False
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    