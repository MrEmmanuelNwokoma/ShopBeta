from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr
from src.models.user_products import UserProducts
from src.models.price_alert import PriceAlert


class User(Basemodel, Base):
    __tablename__="users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    last_login: mapped_column[str] = mapped_column(nullable=False)



    #relationships
    products: Mapped[list["PriceAlert"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    