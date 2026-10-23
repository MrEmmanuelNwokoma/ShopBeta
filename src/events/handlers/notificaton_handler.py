from src.tasks.notification_tasks import create_notification
from src.events.notification_event import NotificationCreatedEvent

async def handle_notification_created(event: NotificationCreatedEvent):
    print("notification handler called", event)
    assert isinstance(event, NotificationCreatedEvent)
    notification_data = event.data
    recipient_ids = [event.recipient_id]

    return create_notification.delay(notification_data=notification_data.model_dump(), recipient_ids=recipient_ids) 