from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.product import Product

class PriceAlert(Basemodel, Base):
    __tablename__="price_alerts"


    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False)
    target_price: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)




    #relationships
    user: Mapped["User"] = relationship(back_populates="products")

    product: Mapped["Product"] = relationship(back_populates="users")