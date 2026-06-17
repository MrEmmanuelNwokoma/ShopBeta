from celery_app import celery_app
from src.schemas.notification import CreateNotification
from src.storage import sync_db
from src.unit_of_work.sync_unit_of_work import SyncUnitOfWork
from src.services.sync_notification_service import SyncNotificationService



@celery_app.task(bind=True, name="create_notification_task")
def create_notification(self, notification_data: dict, recipient_ids: list[str]):

    data = CreateNotification(**notification_data)

    try:
        with sync_db.get_session() as session:
            uow_factory = SyncUnitOfWork(session)
            notification_service = SyncNotificationService(uow_factory)
            notification_service.create_notification(data, recipient_ids)
    except Exception as e:
        self.retry(exc=e, countdown=5)
    return "Notificaiton created successfully"
