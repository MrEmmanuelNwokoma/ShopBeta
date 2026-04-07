from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base
from src.enums.enums import NotificationType


if TYPE_CHECKING:
    from src.models.user import User
    from src.models.notification_recipient import Notification

class Notification(Basemodel, Base):
    __tablename__="notifications"

    sender_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    notifcation_type: Mapped[str] = mapped_column(Enum(NotificationType), nullable=False)



    sender: Mapped["User"] = relationship(back_populates="sent_notifications")

    recipients: Mapped[""]