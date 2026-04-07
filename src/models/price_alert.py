from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.store_product import StoreProduct

class PriceAlert(Basemodel, Base):
    __tablename__="price_alerts"


    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    store_product_id: Mapped[str] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    target_price: Mapped[float] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_triggered: Mapped[bool] = mapped_column(default=False)
    is_triggered_at: Mapped[datetime] = mapped_column(default=False)
    




    #relationships
    user: Mapped["User"] = relationship(back_populates="products")

    store_product: Mapped["StoreProduct"] = relationship(back_populates="price_alerts")