from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.store_product import StoreProduct
from src.repositories.base import BaseRepository

class StoreProductRepository(BaseRepository[StoreProduct]):
    def __init__(self, session: AsyncSession):
        super().__init__(StoreProduct, session)

    async def get_store_product(self, store_id: str, product_id: str):
        stmt =( 
            select(self.model)
            .options(
                selectinload(self.model.store_product_images),
                joinedload(self.model.store),
                joinedload(self.model.product).joinedload(self.model.product.brand)
            )
            .where(
            self.model.store_id == store_id,
            self.model.product_id == product_id
        )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all

    async def get_by_store_and_product_ids(self, store_id: str, product_ids: list[str]):
        stmt = select(self.model).where(
            self.model.store_id == store_id,
            self.model.product_id.in_(product_ids)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    # async def get_product_prices(self, product_id: str):
    #     stmt = select(self.model).where(self.model.product_id == product_id)
    #     result = await self.session.execute(stmt)
    #     return result.scalars().all()

    async def bulk_update(self, store_products: list[StoreProduct]) -> None:
            """Executes a bulk UPDATE query for a list of modified model instances."""
            if not store_products:
                return

            # Extract primary key and updated attributes into parameter mappings
            mappings = [
                {
                    "id": store_product.id,
                    "store_id": store_product.store_id,
                    "product_id": store_product.product_id,
                    "price": store_product.price,
                    "currency": store_product.currency,
                    "product_url": store_product.product_url,
                }
                for store_product in store_products
            ]

            # Generates a single parameterized UPDATE statement using DB-API executemany
            stmt = update(StoreProduct)
            results = await self.session.execute(stmt, mappings)
            return len(store_products) 

    