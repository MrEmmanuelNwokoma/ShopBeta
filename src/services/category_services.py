from src.unit_of_work.unit_of_work import UnitOfWork


class CategoryService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
    
    async def get_categories(self):
            categories = await self.uow_factory.category_repo.get_categories()
            if not categories:
                return []
            return {
                "status": "success",
                "message": "Categories successfully retrieved",
                "data": categories
            }
    
    async def get_category_products(self, id: str):
        category_products = await self.uow_factory.category_repo.get_category_products(id)
        if not category_products:
            return {
                "status": "success",
                "message": "No products found for this category",
                "data": []
            }
        return {
            "status": "success",
            "message": "Products successfully retrieved for this category",
            "data": category_products
        }