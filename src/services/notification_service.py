from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.notification import CreateNotification
from src.models.notification_recipient import NotificationRecipient
from src.integrations.firebase import firebase_client





class NotificationService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    async def create_notification(
    self,
    notification_data: CreateNotification,
    recipient_ids: list[str] | None = None,
):

        # 1. Save everything first; the UoW commits when this block exits
        async with self.uow_factory as uow:
            new_notification = await uow.notification_repo.create_notification(
                notification_data
            )
            notification_id = new_notification.id

            if recipient_ids:
                recipients = [
                    NotificationRecipient(
                        notification_id=notification_id,
                        recipient_id=recipient_id,
                    )
                    for recipient_id in recipient_ids
                ]
                await uow.notification_recipient_repo.bulk_create(recipients)

                devices = await uow.device_token_repo.get_devices(recipient_ids)
                tokens = [device.token for device in devices]
            else:
                tokens = []

        # 2. Send after the commit, outside the UoW
        if tokens:
            invalid = await firebase_client.send_notification(
                tokens,
                notification_data.title,
                notification_data.message,
                notification_data.meta_data,
            )

            # 3. Clean up dead tokens in a fresh UoW
            if invalid:
                async with self.uow_factory as uow:
                    await uow.device_token_repo.delete_by_tokens(invalid)

        return notification_id
            
            