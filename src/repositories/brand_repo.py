from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.brand import Brand
from src.schemas.brand_schema import CreateBrand


class BrandRepository(BaseRepository[Brand]):
    def __init__(self, session: AsyncSession):
        super().__init__(Brand, session)
    
    async def add_brand(self, brand_data: CreateBrand):
        data = brand_data.model_dump()
        brand = Brand(**data)
        new_brand = await self.create(brand)
        return new_brand
    
    async def get_by_name(self, name: str):
        stmt = select(self.model).where(self.model.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
