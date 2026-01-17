from src.models.base import Basemodel, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.user import User
from src.models.product import Product


class PriceAlert(Basemodel, Base):
    __tablename__="price_alerts"


    user_id: Mapped[str] = mapped_column(nullable=False)
    product_id: Mapped[str] = mapped_column(nullable=False)
    target_price: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)




    #relationships
    user: Mapped["User"] = relationship(back_populates="products", cascade="all, delete-orphan")

    product: Mapped["Product"] = relationship(back_populates="users", cascade="all, delete-orphan")