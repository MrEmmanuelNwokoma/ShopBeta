from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from src.repositories.base import BaseRepository
from src.models.product import Product
from src.schemas.product_schema import CreateProduct, UpdateProduct



class ProductRepository(BaseRepository[Product]):
    "Product repository"
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
    
    async def get_brand(self, brand: str):
        result = await self.session.execute(select(self.model).where(self.model.brand == brand))
        return result.scalars().all()
    
    async def create_product(self, product_data: CreateProduct):
        data = product_data.model_dump()
        data["product_url"] = str(data["product_url"])
        product = Product(**data)
        new_product = await self.create(product)
        return new_product
    
    async def bulk_create_products(self, products_data: list[CreateProduct]):
        products = []

        for product_data in products_data:
            data = product_data.model_dump()
            if "product_url" in data:
                data["product_url"] = str(data["product_url"])
            products.append(Product(**data))
        await self.bulk_create(products)
        return products
    
    async def get_multiple_products(self, product_ids: list[str]):
        stmt = select(self.model).where(self.model.id.in_(product_ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_product(self, product_id: str, product_data: UpdateProduct):
        
        data = product_data.model_dump()
        data["product_url"] = str(data["product_url"])
        updated_product = await self.update(id=product_id, data=data)
        return updated_product
    
    async def bulk_delete_products(self, product_ids: list[str]):
        
        count_stmt = select(func.count()).where(self.model.id.in_(product_ids))
        count = await self.session.execute(count_stmt)
        total = count.scalar_one()
        stmt = delete(self.model).where(self.model.id.in_(product_ids))
        await self.session.execute(stmt)
        return total

    