from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr
from src.models.price_alert import PriceAlert


class User(Basemodel, Base):
    __tablename__="users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    soft_delete: Mapped[bool] = mapped_column(nullable=False, default=False)
    reset_token: Mapped[str] = mapped_column(default=False, nullable=True)
    last_login: Mapped[str] = mapped_column(nullable=False)



    #relationships
    products: Mapped[list["PriceAlert"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    