from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from src.models.base import Basemodel, Base


if TYPE_CHECKING:
    from src.models.brand import Brand


class BrandSignal(Basemodel, Base):
    __tablename__="brand_signals"
    brand_id: Mapped[str] = mapped_column(ForeignKey("brands.id"), nullable=False)
    signal: Mapped[str] = mapped_column(nullable=False)



    brand: Mapped["Brand"] = relationship(back_populates="brand_signals")