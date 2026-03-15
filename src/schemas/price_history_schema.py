from pydantic import BaseModel, ConfigDict

class BasePriceHistory(BaseModel):
    price: float


class CreatePriceHistory(BasePriceHistory):
    store_product_id: str

    @classmethod
    def from_store_product(cls, new_store_product):
        return cls(
            store_product_id=str(new_store_product.id),
            price=str(new_store_product.price)
        )
    
class ReadPriceHistory(BasePriceHistory):
    """Read price history"""

    model_config = ConfigDict(from_attributes=True)
