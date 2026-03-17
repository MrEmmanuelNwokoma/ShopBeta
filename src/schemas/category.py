from pydantic import BaseModel



class BaseCategory(BaseModel):
    name: str



class CreateCategory(BaseCategory):
    """create a category"""

class ReadCategory(BaseCategory):
    """read category"""
