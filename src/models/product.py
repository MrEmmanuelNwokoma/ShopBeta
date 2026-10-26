from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR

from decimal import Decimal
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base



if TYPE_CHECKING:
    from models.store_product import StoreProduct
    from src.models.category import Category
    
    from src.models.brand import Brand

class Product(Basemodel, Base):
    __tablename__="products"
    __table_args__ = (
        Index('ix_products_search_vector',
              'search_vector', postgresql_using='gin'),
    )
    
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    ram: Mapped[str] = mapped_column(nullable=True)
    storage: Mapped[str] = mapped_column(nullable=True)
    brand_id: Mapped[str] = mapped_column(ForeignKey("brands.id"), nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)

    if Base.metadata.info.get("bind") and Base.metadata.info["bind"].dialect.name == "postgresql":
        search_vector: Mapped[str] = mapped_column(
            TSVECTOR,
            nullable=False,
            server_default=Computed(
                "to_tsvector('english', "
                "coalesce(ram, '') || ' ' || "
                "coalesce(storage, '') || ' ' || "
                "coalesce(model, '') || ' ' || "
                ")",
                persisted=True
            ),
        )
    else:
        # SQLite fallback
        search_vector: Mapped[str] = mapped_column(nullable=True)
    


    
    #relationships
    category: Mapped["Category"] = relationship(back_populates="products")
    stores: Mapped[list["StoreProduct"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    
    brand: Mapped["Brand"] = relationship(back_populates="products", lazy="raise")



    @property
    def display_name(self):
        parts = [
            self.brand.name,
            self.model, 
            f"{self.ram} RAM" if self.ram else None, 
            f"{self.storage} Storage" if self.storage else None
        ]
        return " ".join(part for part in parts if part)

    @property
    def store_products_count(self) -> int:
        return len(self.stores) if self.stores else 0

    @property
    def product_image(self):
        for store_product in self.stores:
            if store_product.store_product_images:
                return store_product.store_product_images[0]
