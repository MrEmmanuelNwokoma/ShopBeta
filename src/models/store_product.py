from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.models.store import Store
from src.models.product import Product


class StoreProduct(Basemodel, Base):
    __tablename__="prices"


    price: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    # product_url: Mapped[str] = mapped_column(nullable=False)
    instock: Mapped[str] = mapped_column(nullable=False)


    store: Mapped["Store"] = relationship(back_populates="products")
    product: Mapped["Product"] = relationship(back_populates="stores")

