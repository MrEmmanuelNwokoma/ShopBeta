from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class BasePriceHistory(BaseModel):
    price: Decimal
    store_product_id: str

class CreatePriceHistory(BasePriceHistory):
    """Create price history"""

    @classmethod
    def from_store_product(cls, store_product):
        return cls(
            store_product_id=str(store_product.id),
            price=str(store_product.price)
        )
    
class ReadPriceHistory(BasePriceHistory):
    """Read price history"""

    model_config = ConfigDict(from_attributes=True)
