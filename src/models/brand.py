from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base


if TYPE_CHECKING:
    from src.models.brand_signals import BrandSignal
    from src.models.product import Product

class Brand(Basemodel, Base):
    __tablename__="brands"
    name: Mapped[str] = mapped_column(nullable=False)
    
    brand_signals: Mapped[list["BrandSignal"]] = relationship(back_populates="brand")
    products: Mapped[list["Product"]] = relationship(back_populates="brand", cascade="all, delete-orphan")