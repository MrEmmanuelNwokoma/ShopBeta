from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.brand_signals import BrandSignal


class BrandSignalRepository(BaseRepository[BrandSignal]):
    def __init__(self, session: AsyncSession):
        super().__init__(BrandSignal, session)
    
