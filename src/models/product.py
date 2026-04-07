from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base



if TYPE_CHECKING:
    from models.store_product import StoreProduct
    from src.models.category import Category
    from src.models.product_image import ProductImage

class Product(Basemodel, Base):
    __tablename__="products"
    
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)



    #relationships
    category: Mapped["Category"] = relationship(back_populates="products")
    stores: Mapped[list["StoreProduct"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    product_images: Mapped[list["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    