from pydantic import BaseModel, ConfigDict




class BaseCategory(BaseModel):
    name: str

    



class CreateCategory(BaseCategory):
    """create a category"""

class ReadCategory(BaseCategory):
    """read category"""
    id: str
    category_image: str | None = None 
    product_count: int | None = None  

    model_config  = ConfigDict(from_attributes=True)
