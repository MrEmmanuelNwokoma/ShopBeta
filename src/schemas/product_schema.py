"""
Pydantic schema for validation
"""
from pydantic import BaseModel, HttpUrl, ConfigDict



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

    model_config  = ConfigDict(from_attributes=True)

class UpdateProduct(BaseProduct):
    """Schema for updating store"""