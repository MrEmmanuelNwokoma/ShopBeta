from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base

if TYPE_CHECKING:
    from src.models.product import Product



if TYPE_CHECKING:
    from src.models.product import Product

class Category(Basemodel, Base):
    __tablename__="categories"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    

    products: Mapped[list["Product"]] = relationship(back_populates="category", cascade="all, delete-orphan")



    @property
    def category_image(self):
        if self.products:
            for product in self.products:
                if product.stores:
                    for store_product in product.stores:
                        if store_product.store_product_images:
                            return store_product.store_product_images[0].store_product_image_url
    
    @property
    def product_count(self):
        if self.products:
            return len(self.products)