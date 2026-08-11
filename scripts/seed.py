from src.storage import db
import asyncio
from src.unit_of_work.unit_of_work import UnitOfWork
from scripts.data import CATEGORIES, STORES, ADMIN_USERS, CANONICAL_BRANDS, BRAND_SIGNALS
from src.auth.security import hash_password
from src.repositories.user_repo import UserRepository
from src.repositories.category_repo import CategoryRepository
from src.repositories.store_repo import StoreRepository
from src.repositories.product_repo import ProductRepository
from src.repositories.brand_repo import BrandRepository
from src.repositories.brand_signal_repo import BrandSignalRepository
from src.models.category import Category
from src.models.store import Store
from src.models.product import Product
from src.models.brand_signals import BrandSignal
from src.models.user import User
from src.models.brand import Brand

async def seed_data():
    await db.drop_tables()
    await db.create_tables()

    async with db.get_session() as session:
        # uow = UnitOfWork(session)
        user_repo = UserRepository(session)
        
        users = []
        for admin_user in ADMIN_USERS:
            admin_user["password"] = hash_password(admin_user["password"])
            users.append(User(**admin_user))
        await user_repo.bulk_create(users)

        brand_repo = BrandRepository(session)
        
        brands = []
        for brand in CANONICAL_BRANDS:
            brands.append(Brand(**brand))
        await brand_repo.bulk_create(brands)
        await session.commit()


        brand_signals_repo = BrandSignalRepository(session)
        brand_signals = []
        for brand_data in BRAND_SIGNALS:
            brand = await brand_repo.get_by_name(brand_data["brand"])
            if not brand:
                continue
            for signal in brand_data["signals"]:
                brand_signals.append(BrandSignal(
                    brand_id=brand.id,
                    signal=signal
                ))
        await brand_signals_repo.bulk_create(brand_signals)

        category_repo = CategoryRepository(session)
        
        categories = []
        for category in CATEGORIES:

            categories.append(Category(**category))

        await category_repo.bulk_create(categories)
        await session.commit()

        store_repo = StoreRepository(session)
        
        stores = []
        for store in STORES:

            stores.append(Store(**store))

        await store_repo.bulk_create(stores)
        await session.commit()

        category_map = {cat.name: cat.id for cat in categories}
        # product_repo = ProductRepository(session)
        
        # products = []
        # for product in PRODUCTS:
        #     category_name = product.pop("category")
        #     print(f"Trying to map", {category_name})
        #     category_id = category_map.get(category_name)
        #     print(f"{category_id}")
        #     if not category_id:
        #         raise ValueError("Id not of found")
        #     product["category_id"] = category_id
            
        #     products.append(Product(**product))
            

        # await product_repo.bulk_create(products)

        await session.commit()
        print("Seeding completed successfully")




if __name__ == "__main__":
    asyncio.run(seed_data())
