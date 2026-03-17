from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.category import Category
from src.schemas.category import CreateCategory, ReadCategory

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
    

    async def create_category(self, category_data: CreateCategory):
        data = category_data.model_dump()
        category = Category(**data)
        new_category = await self.create(category)
        return new_category
    
    async def get_categories(self):
        categories = await self.get_all()
        return categories
    
    
