from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.store_schema import CreateStore, ReadStore, UpdateStore
from src.enums.enums import UserRole
from src.models.user import User
from src.core.exceptions import PermissionDenied


class StoreService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    
    async def create_store(self, current_user: User, store_data: CreateStore):
        if current_user.role != UserRole.ADMIN:
            raise PermissionDenied(
                details={
                    "recommendations": "Make sure you are an admin"
                }
            )
        async with self.uow_factory:
            new_store = await self.uow_factory.store_repo.create_store(store_data)
        return {
            "status": "success",
            "message": "Store successfully created",
            "data": ReadStore.model_validate(new_store)
        }


    async def get_all_stores(self):
        async with self.uow_factory:
            stores = await self.uow_factory.store_repo.get_all()

        return {
            "status": "success",
            "message": "Stores successfully retrieved",
            "data": [ReadStore.model_validate(store) for store in stores]
        }
    
    
    async def get_single_store(self, store_id: str):
        async with self.uow_factory:
            store = await self.uow_factory.store_repo.get_by_id(store_id)
        return {
            "status": "success",
            "message": "Store successfully retrieved",
            "data": ReadStore.model_validate(store)
        }
    

    async def update_store(self, current_user: User, store_id: str, store_data: UpdateStore):
        if current_user.role != UserRole.ADMIN:
            raise PermissionDenied(
                details={
                    "recommendations": "Make sure you are an admin"
                }
            )
        async with self.uow_factory:
            updated_store = await self.uow_factory.store_repo.update_store(store_id, store_data)

        return {
            "status": "success",
            "message": "Store successfully updated",
            "data": ReadStore.model_validate(updated_store)
        }
    
    async def deactivate_store(self, current_user: User, store_id: str):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    details={
                        "recommendations": "Make sure you are an admin"
                    }
                )
            
            await self.uow_factory.store_repo.delete(store_id, soft=True)
        return {
            "status": "success",
            "message": "Store successfully deactivated",
        }
    
