from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models.base import Basemodel, Base 

if TYPE_CHECKING:
    from src.models.user import User


class DeviceToken(Basemodel, Base):
    __tablename__="device_tokens"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    platform: Mapped[str] = mapped_column(nullable=False)


    user: Mapped["User"] = relationship(back_populates="device_tokens")