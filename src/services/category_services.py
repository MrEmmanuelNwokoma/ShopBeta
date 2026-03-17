from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.category import Category

class CategoryService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    
    async def get_categories(self):
        async with self.uow_factory:
            categories = await self.uow_factory.category_repo.get_categories()
            if not categories:
                return []
        return categories
    
    