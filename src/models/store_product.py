from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base
from sqlalchemy import String

if TYPE_CHECKING:
    from src.models.store import Store
    from src.models.product import Product


class StoreProduct(Basemodel, Base):
    __tablename__="store_products"

    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    # product_url: Mapped[str] = mapped_column(nullable=False)
    instock: Mapped[str] = mapped_column(nullable=False)


    store: Mapped["Store"] = relationship(back_populates="products")
    product: Mapped["Product"] = relationship(back_populates="stores")

