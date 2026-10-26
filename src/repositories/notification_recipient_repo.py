from sqlalchemy.orm import Session
from sqlalchemy import select, update
from datetime import datetime, timezone
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

    async def mark_all_as_read(self, user_id: str) -> int:
        stmt = (
            update(NotificationRecipient)
            .where(
                NotificationRecipient.recipient_id == user_id,
                NotificationRecipient.is_read.is_(False),
            )
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        result = await self.session.execute(stmt)
        return result.rowcount