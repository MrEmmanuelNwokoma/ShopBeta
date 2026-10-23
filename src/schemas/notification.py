from pydantic import BaseModel
from datetime import datetime
from src.enums.enums import NotificationType

class CreateNotification(BaseModel):
    title: str
    message: str
    notification_type: NotificationType
    resource_id: str | None = None
    meta_data: dict | None = None



class NotificationContent(BaseModel):
    id: str
    title: str
    message: str
    meta_data: dict | None = None
    notification_type: str
    resource_id: str | None = None
    created_at: datetime

    