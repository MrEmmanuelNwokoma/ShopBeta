from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.category import Category
from src.schemas.category import CreateCategory, ReadCategory
from src.models.product import Product
from src.models.store_product import StoreProduct


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
    

    async def create_category(self, category_data: CreateCategory):
        data = category_data.model_dump()
        category = Category(**data)
        new_category = await self.create(category)
        return new_category
    
    async def get_category_products(self, id: str):
        stmt = select(Category).where(Category.id == id).options(
            selectinload(Category.products).options(
                selectinload(Product.brand),
                selectinload(Product.stores).options(
                    selectinload(StoreProduct.store_product_images),
                    joinedload(StoreProduct.store)  # <-- Add this here!
                )
            )
        )
        result = await self.session.execute(stmt)
        category = result.scalars().first()
        if not category:
            return None
        return category.products
        
    
    async def get_categories(self):
        stmt = select(Category).options(

            selectinload(Category.products)
            .selectinload(Product.stores) 
            .selectinload(StoreProduct.store_product_images)
        )
        result = await self.session.execute(stmt)
        categories = result.scalars().unique().all()
        return categories
    
    
