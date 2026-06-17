"""
Pydantic schemas for validation
"""
from pydantic import BaseModel, ConfigDict
from src.schemas.product_schema import ReadProduct
from src.schemas.store_schema import ReadStore


class BaseStoreProduct(BaseModel):
    """Base store_product schema """
    price: str
    currency: str


class ReadStoreProduct(BaseStoreProduct):
    """Schema for reading store_product"""
    store: ReadStore
    product: ReadProduct
    instock: bool

    model_config = ConfigDict(from_attributes=True)


class CreateStoreProduct(BaseStoreProduct):
    """Schema for creating store_product relationship"""
    store_id: str
    product_id: str