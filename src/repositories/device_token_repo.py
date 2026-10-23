from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.repositories.base import BaseRepository
from src.models.device_tokens import DeviceToken
from src.schemas.device_token_schema import AddDeviceToken


class DeviceTokenRepository(BaseRepository[DeviceToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(DeviceToken, session)

    async def add_device_token(self, device_data: AddDeviceToken):
        data = DeviceToken(**device_data.model_dump())
        device = await self.create(data)
        return device
    
    async def get_user_devices(self, user_id: str):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_devices(self, user_ids: list[str]):
        stmt = select(self.model).where(self.model.user_id.in_(user_ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def delete_by_tokens(self, tokens: list[str]) -> int:
        result = await self.session.execute(
            delete(self.model).where(self.model.token.in_(tokens))
        )
        return result.rowcount
    

    