from sqlalchemy.orm import Session
from src.models.notification_recipient import NotificationRecipient

from src.repositories.sync_base import SyncBaseRepository

class SyncNotificationRecipientRepository(SyncBaseRepository[NotificationRecipient]):
    def __init__(self, session: Session):
        super().__init__(NotificationRecipient, session)