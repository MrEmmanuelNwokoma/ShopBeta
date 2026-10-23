from sqlalchemy.orm import Session
from src.models.notification import Notification
from src.schemas.notification import CreateNotification
from src.repositories.base import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: Session):
        super().__init__(Notification, session)
    
    def create_notification(self, notification_data: CreateNotification):
        data = notification_data.model_dump()
        notification = Notification(**data)
        new_notification = self.create(notification)
        return new_notification
    

