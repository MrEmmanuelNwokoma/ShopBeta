from pydantic import BaseModel
from datetime import datetime
from src.schemas.notification import NotificationContent




class ReadNotification(BaseModel):
    id: str                         
    notification_id: str
    is_read: bool = False
    read_at: datetime | None = None
    created_at: datetime
    recipient_id: str
    notification: NotificationContent