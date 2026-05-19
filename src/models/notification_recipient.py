from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base


if TYPE_CHECKING:
    from src.models.user import User
    from src.models.notification import Notification

class NotificationRecipient(Basemodel, Base):
    __tablename__="notification_recipients"



    recipient_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)



    # notification: Mapped["Notification"] = relationship(back_populates="recipients")
    # user: Mapped["User"] = relationship(back_populates="notification_recipients")

