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