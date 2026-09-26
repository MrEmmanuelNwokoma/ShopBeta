from pydantic import BaseModel
from pydantic import BaseModel, HttpUrl, ConfigDict


class CreateBrand(BaseModel):
    name: str


class ReadBrand(CreateBrand):
    """Schema for reading brand"""
    id: str

    model_config = ConfigDict(from_attributes=True)