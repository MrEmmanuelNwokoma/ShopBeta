from sqlalchemy import ForeignKey, Table, Column
from src.models.base import Basemodel,Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models.user import User
from src.models.product import Product


class UserProducts(Basemodel, Base):
    __tablename__ ="user_products"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))


    users: Mapped["User"] = relationship(back_populates="space_amenities")

    products: Mapped["Product"] = relationship(back_populates="space_amenities")
    