"""
Pydantic schemas for validation
"""
from pydantic import BaseModel, ConfigDict, HttpUrl
from decimal import Decimal
from src.schemas.store_schema import ReadStore


class BaseStoreProduct(BaseModel):
    """Base store_product schema """
    price: Decimal
    currency: str
    product_url: HttpUrl



class ReadStoreProduct(BaseStoreProduct):
    """Schema for reading store_product"""
    id: str
    name: str
    price: float
    currency: str
    product_url: str
    store: ReadStore  # The nested store details (e.g., Jumia, Konga, Slot)
    

    model_config = ConfigDict(from_attributes=True)

    model_config = ConfigDict(from_attributes=True)


class CreateStoreProduct(BaseStoreProduct):
    """Schema for creating store_product relationship"""
    store_id: str
    product_id: str
    