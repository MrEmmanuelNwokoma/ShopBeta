from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic


T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    """Wrapper for product response"""
    status: str
    message: str
    data: T

    
    model_config  = ConfigDict(from_attributes=True)