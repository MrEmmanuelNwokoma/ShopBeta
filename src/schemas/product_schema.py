"""
Pydantic schema for validation
"""
from pydantic import BaseModel, HttpUrl



class BaseProduct(BaseModel):
    """Parent store schema which other store schemas inherit"""
    name: str
    brand: str
    description: str
    product_url: HttpUrl

class CreateProduct(BaseProduct):
    """Schema for creating a product"""
    
class ReadProduct(BaseProduct):
    """Schema for reading product"""
    id: str

class UpdateProduct(BaseProduct):
    """Schema for updating store"""