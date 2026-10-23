from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.device_token_schema import AddDeviceToken



class DeviceTokenService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    

    async def add_device_token(self, device_data: AddDeviceToken, user_id: str):
        async with self.uow_factory as uow:
            return await uow.device_token_repo.add_device_token(device_data, user_id)

    async def delete_device_tokens(self, tokens: list[str]):
        async with self.uow_factory as uow:
            return await uow.device_token_repo.delete_by_tokens(tokens)

    async def get_user_devices(self, user_id: str):
        async with self.uow_factory as uow:
            return await uow.device_token_repo.get_user_devices(user_id)
    
    