from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    
    from src.models.store_product import StoreProduct


class StoreProductImage(Basemodel, Base):
    __tablename__="store_product_images"

    store_product_id: Mapped[str] = mapped_column(ForeignKey("store_products.id"))
    store_product_image_url: Mapped[str] = mapped_column(nullable=False)

    
    store_product: Mapped["StoreProduct"] = relationship(back_populates="store_product_images")