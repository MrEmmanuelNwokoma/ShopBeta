import asyncio
from celery_app import celery_app
from src.schemas.notification import CreateNotification
from src.storage import db
from src.unit_of_work.unit_of_work import UnitOfWork
from src.services.notification_service import NotificationService




@celery_app.task(
    bind=True,
    name="create_notification_task",
    max_retries=3,
)
def create_notification(self, notification_data: dict, recipient_ids: list[str]):
    data = CreateNotification(**notification_data)

    async def _run():
        async with db.get_session() as session:
            uow = UnitOfWork(session)
            service = NotificationService(uow)
            await service.create_notification(data, recipient_ids)

    try:
        asyncio.run(_run())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
