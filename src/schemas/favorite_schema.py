from pydantic import BaseModel

class CreateFavorites(BaseModel):
    store_product_id: str

class ReadFavorites(BaseModel):
    user_name: str
    store_product_name: str

