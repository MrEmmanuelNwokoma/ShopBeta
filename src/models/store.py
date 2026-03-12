from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.store_product import StoreProduct

class Store(Basemodel, Base):
    __tablename__="stores"

    name: Mapped[str] = mapped_column(nullable=False)
    supports_api: Mapped[bool] = mapped_column(nullable=False, default=False)
    website_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)



    products: Mapped[list["StoreProduct"]] = relationship(back_populates="store")
     
