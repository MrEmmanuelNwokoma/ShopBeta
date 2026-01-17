from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.user_products import UserProducts
from src.models.price_alert import PriceAlert
from models.store_product import StoreProduct

class Product(Basemodel, Base):
    __tablename__="products"

    name: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    product_url: Mapped[str] = mapped_column(nullable=False)



    #relationships
    users: Mapped[list["PriceAlert"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

    store: Mapped[list["StoreProduct"]] = relationship(back_populates="product", cascade="all, delete-orphan")