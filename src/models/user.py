from src.models.base import Basemodel, Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, DateTime
from typing import TYPE_CHECKING
from src.models.price_alert import PriceAlert
from src.models.favorites import Favorite

from src.enums.enums import UserRole

if TYPE_CHECKING:
    from src.models.notification import Notification
    from src.models.notification_recipient import NotificationRecipient
    from src.models.device_tokens import DeviceToken


class User(Basemodel, Base):
    __tablename__="users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.ADMIN)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    verification_token: Mapped[str] = mapped_column(nullable=True)
    verification_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    last_login: Mapped[str] = mapped_column(nullable=True)



    #relationships
    products: Mapped[list["PriceAlert"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    sent_notifications: Mapped[list["Notification"]] = relationship(
        back_populates="sender"
    )

    # notification_recipients: Mapped[list["NotificationRecipient"]] = relationship(back_populates="user")
    device_tokens: Mapped[list["DeviceToken"]] = relationship(
        back_populates="user"
    )
    
