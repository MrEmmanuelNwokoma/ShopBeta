from src.schemas.user_schema import ReadUser, UpdateUser
from src.unit_of_work.unit_of_work import UnitOfWork


class UserService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
      

    async def update_user(self, user_data: UpdateUser, user_id: str):
        data = user_data.model_dump()
        async with self.uow_factory:
            await self.uow_factory.user_repo.update(user_id, data)
            return user_data
        
