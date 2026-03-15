"""
Pydantic schema for validation
"""
from pydantic import BaseModel, AnyHttpUrl, ConfigDict


class BaseStore(BaseModel):
    """Parent store schema which other store schemas inherit"""
    name: str
    website_url: AnyHttpUrl
    is_active: bool = True
    supports_api: bool = False


class CreateStore(BaseStore):
    """Schema for creating a store"""


class ReadStore(BaseStore):
    """Schema for reading store"""

    model_config = ConfigDict(from_attributes=True)

class UpdateStore(BaseStore):
    """Schema for updating store"""
    