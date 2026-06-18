from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import ForeignKey, DateTime
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.store_product import StoreProduct

class PriceAlert(Basemodel, Base):
    __tablename__="price_alerts"


    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    store_product_id: Mapped[str] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    target_price: Mapped[Decimal] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_triggered: Mapped[bool] = mapped_column(default=False)
    is_triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone), nullable=False,  default=datetime.now(timezone.utc))
    




    #relationships
    user: Mapped["User"] = relationship(back_populates="products")

    store_product: Mapped["StoreProduct"] = relationship(back_populates="price_alerts")