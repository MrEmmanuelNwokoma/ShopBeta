from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from decimal import Decimal
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base
from sqlalchemy import String

if TYPE_CHECKING:
    from src.models.store import Store
    from src.models.product import Product
    from src.models.price_alert import PriceAlert
    from src.models.price_history import PriceHistory
    from src.models.favorites import Favorite


class StoreProduct(Basemodel, Base):
    __tablename__="store_products"

    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    instock: Mapped[bool] = mapped_column(nullable=False, default=True)
    


    store: Mapped["Store"] = relationship(back_populates="products")
    price_alerts: Mapped[list["PriceAlert"]] = relationship(back_populates="store_product", cascade="all, delete-orphan")
    product: Mapped["Product"] = relationship(back_populates="stores")
    price_histories: Mapped[list["PriceHistory"]] = relationship(back_populates="store_product", cascade="all, delete-orphan")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="store_product", cascade="all, delete-orphan")
