from sqlalchemy.ext.asyncio import AsyncSession
from src.events.bus import event_bus
from src.events.base import DomainEvent
from src.repositories.store_repo import StoreRepository
from src.repositories.store_product_repo import StoreProductRepository
from src.repositories.product_repo import ProductRepository
from src.repositories.user_repo import UserRepository
from src.repositories.price_histories_repo import PriceHistoryRepository
from src.repositories.price_alert_repo import PriceAlertRepository
from src.repositories.category_repo import CategoryRepository
from src.repositories.favorites_repo import FavoriteRepository
from src.repositories.device_token_repo import DeviceTokenRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_bus = event_bus
        self._pending_event: list[DomainEvent] = []

        self.user_repo = UserRepository(session)
        self.store_repo = StoreRepository(session)
        self.product_repo = ProductRepository(session)
        self.store_product_repo = StoreProductRepository(session)
        self.price_history_repo = PriceHistoryRepository(session)
        self.price_alert_repo = PriceAlertRepository(session)
        self.category_repo = CategoryRepository(session)
        self.favorite_repo = FavoriteRepository(session)
        self.device_token_repo = DeviceTokenRepository(session)
        
    async def collect_event(self, event: DomainEvent):
        self._pending_event.append(event)
    
    async def __aenter__(self):
        # await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
            self._pending_event.clear()
            await self.session.close()
        else:
            await self.session.commit()

        if self.event_bus:
            for ev in self._pending_event:
                await self.event_bus.publish_event(ev)
