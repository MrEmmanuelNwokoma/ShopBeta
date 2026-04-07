"""
Pydantic schema for validation
"""
from pydantic import BaseModel, HttpUrl, ConfigDict



class BaseProduct(BaseModel):
    """Parent store schema which other store schemas inherit"""
    name: str
    brand: str
    description: str
    
    

class CreateProduct(BaseProduct):
    """Schema for creating a product"""
    category_id: str
    
class ReadProduct(BaseProduct):
    id: str
    """Schema for reading product"""

    model_config  = ConfigDict(from_attributes=True)

class UpdateProduct(BaseProduct):
    """Schema for updating store"""
    