from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.product import Product


class ProductImage(Basemodel, Base):
    __tablename__="product_images"

    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    order: Mapped[int] = mapped_column(nullable=False, default=0)

    product: Mapped["Product"] = relationship(back_populates="product_images")