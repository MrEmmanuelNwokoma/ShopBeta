"""
Pydantic schemas for validation
"""
from pydantic import BaseModel
from src.model_schemas.product_schema import ReadProduct
from src.model_schemas.store_schema import ReadStore


class BaseStoreProduct(BaseModel):
    """Base store_product schema """
    price: str
    instock: str


class ReadStoreProduct(BaseStoreProduct):
    """Schema for reading store_product"""
    store: ReadStore
    product: ReadProduct

class CreateStoreProduct(BaseStoreProduct):
    """Schema for creating store_product relationship"""
    store_id: str
    product_id: str