from src.unit_of_work.sync_unit_of_work import SyncUnitOfWork
from src.schemas.notification import CreateNotification
from src.models.notification_recipient import NotificationRecipient




class SyncNotificationService:
    def __init__(self, uow_factory: SyncUnitOfWork):
        self.uow_factory = uow_factory

    def create_notification(self, notification_data: CreateNotification, recipient_ids: list[str] = []):
        with self.uow_factory as uow:
            recipients = []
            new_notification = uow.sync_notification_repo.create_notification(notification_data)
            
            for recipient_id in recipient_ids:
                notification_recipient = NotificationRecipient(
                    notification_id=new_notification.id,
                    recipient_id=recipient_id
                )
                recipients.append(notification_recipient)
            if recipients:
                uow.sync_notification_recipient_repo.bulk_create(recipients)
            return new_notification
        
        