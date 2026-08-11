from pydantic import BaseModel


class CreateBrand(BaseModel):
    brand_name: str