from src.storage import db
import asyncio
from src.unit_of_work.unit_of_work import UnitOfWork
from scripts.data import CATEGORIES, STORES, ADMIN_USERS
from src.auth.security import hash_password
from src.repositories.user_repo import UserRepository
from src.repositories.category_repo import CategoryRepository
from src.repositories.store_repo import StoreRepository
from src.repositories.product_repo import ProductRepository
from src.models.category import Category
from src.models.store import Store
from src.models.product import Product
from src.models.user import User


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
