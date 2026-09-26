"""
Pydantic schema for validation
"""
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic
from src.schemas.brand_schema import ReadBrand
from src.schemas.store_product_image_schema import StoreProductImage
from src.schemas.store_product import ReadStoreProduct

T = TypeVar("T")

class BaseProduct(BaseModel):
    """Parent store schema which other store schemas inherit"""
    id: str
    ram: str | None
    storage: str | None
    brand: ReadBrand
    
    
    

class CreateProduct(BaseProduct):
    """Schema for creating a product"""
    category_id: str


    
class ReadProduct(BaseProduct):
    """Schema for reading product"""
    
    display_name: str
    store_products_count: int
    product_image: StoreProductImage
    stores: list[ReadStoreProduct] = []


    model_config  = ConfigDict(from_attributes=True)





# class UpdateProduct(BaseProduct):
#     """Schema for updating store"""
    