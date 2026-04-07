from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.store_product import StoreProduct

class Favorite(Basemodel, Base):
    __tablename__="favorites"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    store_product_id: Mapped[str] = mapped_column(ForeignKey("store_products.id"), nullable=False)




    #relationships

    user: Mapped["User"] = relationship(back_populates="favorites")
    store_product: Mapped["StoreProduct"] = relationship(back_populates="favorites")