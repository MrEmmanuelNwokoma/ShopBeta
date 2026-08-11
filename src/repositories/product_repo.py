import logging
from sqlalchemy.ext.asyncio import AsyncSession
from thefuzz import fuzz
from sqlalchemy import select, delete, func
from src.repositories.base import BaseRepository
from src.models.product import Product
from src.schemas.product_schema import CreateProduct, UpdateProduct
from src.utils.text_utils import build_product_signature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductRepository(BaseRepository[Product]):
    "Product repository"
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def bulk_create_products(self, products_data: list[dict]):
        """Match or bulk create products"""
        MATCH_THRESHOLD = 90
        
        # 1. Deduplicate within the batch first
        seen = {}
        unique_products_data = []
        
        for product_data in products_data:
            key = (
                product_data["brand_id"],
                product_data["model"],
                product_data.get("ram"),
                product_data.get("storage")
            )
            
            if key not in seen:
                seen[key] = product_data
                unique_products_data.append(product_data)
            else:
                logger.warning(f"Duplicate in batch: {key}")
        
        # 2. Now match/create against DB
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        existing_products = result.scalars().all()
        
        new_products = []
        matched_products = []

        for product_data in unique_products_data:  # ← Use deduplicated list
            best_score = 0
            best_match = None
            
            # Build signature once per product
            incoming_signature = build_product_signature(
                product_data["model"], 
                product_data.get("ram"), 
                product_data.get("storage")
            )
            
            for product in existing_products:
                existing_signature = build_product_signature(
                    product.model, 
                    product.ram, 
                    product.storage
                )
                score = fuzz.token_sort_ratio(incoming_signature, existing_signature)
                
                if score > best_score:
                    best_score = score
                    best_match = product

            if best_match and best_score >= MATCH_THRESHOLD:
                matched_products.append(best_match)
            else:
                new_products.append(Product(
                    brand_id=product_data["brand_id"],
                    category_id=product_data["category_id"],
                    model=product_data["model"],
                    ram=product_data.get("ram"),
                    storage=product_data.get("storage"),
                ))
        
        if new_products:
            await self.bulk_create(new_products)
        
        return new_products + matched_products
    
    async def get_multiple_products(self, product_ids: list[str]):
        stmt = select(self.model).where(self.model.id.in_(product_ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_brand(self, brand: str):
        result = await self.session.execute(select(self.model).where(self.model.brand == brand))
        return result.scalars().all()
    
    async def get_product_by_name(self, name: str):
        result = await self.session.execute(select(self.model).where(self.model.name == name))
        return result.scalar_one_or_none()
    
    async def get_products_by_category(self, category_id: str):
        stmt = select(self.model).where(self.model.category_id == category_id)
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

    