from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.store_repo import StoreRepository
from src.repositories.product_repo import ProductRepository
from src.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repo = UserRepository(session)
        self.store_repo = StoreRepository(session)
        self.product_repo = ProductRepository(session)
  

    
    async def __aenter__(self):
        # await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()