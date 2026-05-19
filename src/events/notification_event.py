from src.events.base import DomainEvent
from src.schemas.notification import CreateNotification

class NotificationCreatedEvent(DomainEvent):
    data: CreateNotification
    recipient_id: str

    