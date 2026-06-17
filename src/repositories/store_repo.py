from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.store import Store
from src.schemas.store_schema import CreateStore, UpdateStore



class StoreRepository(BaseRepository[Store]):
    "Store repository"
    def __init__(self, session: AsyncSession):
        super().__init__(Store, session)
    
    async def create_store(self, store_data: CreateStore)-> Store:
        data = store_data.model_dump()
        data["website_url"] = str(data["website_url"])
        store = Store(**data)
        new_store = await self.create(store)
        return new_store
    
    
    async def get_by_name(self, name: str):
        result = await self.session.execute(select(self.model).where(self.model.name == name))
        return result.scalar_one_or_none()
    
    async def get_store_by_status(self, is_active: bool)-> list[Store]:
        result = await self.session.execute(select(self.model).where(self.model.is_active.is_(is_active)))
        return result.scalars().all()
    
    async def update_store(self, store_id, store_data: UpdateStore)-> Store:
        data = store_data.model_dump()
        data["website_url"] = str(data["website_url"])
        updated_store = await self.update(id=store_id, data=data)
        return updated_store
   
    
    