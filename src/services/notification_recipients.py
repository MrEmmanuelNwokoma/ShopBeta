from src.unit_of_work.unit_of_work import UnitOfWork
from datetime import datetime, timezone
from src.schemas.notification_recipient import ReadNotification

class NotificationRecipientService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    async def get_user_notifications(self, user_id: str):
        async with self.uow_factory as uow:
            notifications = await uow.notification_recipient_repo.get_user_notifications(user_id)
            return notifications

    async def get_user_notification(self, notification_recipient_id: str):
        async with self.uow_factory as uow:
            notification = await uow.notification_recipient_repo.get_user_notification(notification_recipient_id)
            return ReadNotification(
                id=notification.id,
                notification_id=notification.notification_id,
                recipient_id=notification.recipient_id,
                is_read=notification.is_read,
                read_at=notification.read_at,
                created_at=notification.created_at,
                
                notification={
                    "id": notification.notification.id,
                    "title": notification.notification.title,
                    "message": notification.notification.message,
                    "meta_data": notification.notification.meta_data,
                    "notification_type": notification.notification.notification_type,
                    "resource_id": notification.notification.resource_id,
                    "created_at": notification.notification.created_at,
                    
                }
            )

    async def mark_as_read(self, notification_recipient_id: str, user_id: str):
        async with self.uow_factory as uow:
            notification = await uow.notification_recipient_repo.get_user_notification(notification_recipient_id)
            if not notification:
                return None
            if notification.recipient_id != user_id:
                return None
            data={
                "is_read": True,
                "read_at": datetime.now(timezone.utc)
            }
            await uow.notification_recipient_repo.update(notification_recipient_id, data)
            return notification