from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models.notification_recipient import NotificationRecipient

from src.repositories.base import BaseRepository

class NotificationRecipientRepository(BaseRepository[NotificationRecipient]):
    def __init__(self, session: Session):
        super().__init__(NotificationRecipient, session)

    async def get_user_notifications(self, user_id: str):
        stmt = (
            select(NotificationRecipient)
            .where(NotificationRecipient.recipient_id == user_id)
            .options(joinedload(NotificationRecipient.notification))
            .order_by(NotificationRecipient.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_notification(self, notification_recipient_id: str):
        stmt = (
            select(NotificationRecipient)
            .where(NotificationRecipient.id == notification_recipient_id)
            .options(joinedload(NotificationRecipient.notification))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()