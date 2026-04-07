from sqlalchemy.orm import Session
from src.repositories.sync_notification_repo import SyncNotificationRepository



class SyncUnitOfWork:
    def __init__(self):
        self.session = Session

        self.notification_repo = SyncNotificationRepository

    

    async def __aenter__(self):
        # await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()