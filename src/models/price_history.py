from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from decimal import Decimal
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.store_product import StoreProduct


class PriceHistory(Basemodel, Base):
    __tablename__ = "price_histories"

    store_product_id: Mapped[str] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)

    store_product: Mapped["StoreProduct"] = relationship(back_populates="price_histories")



