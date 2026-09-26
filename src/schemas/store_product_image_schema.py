from pydantic import BaseModel, ConfigDict

class StoreProductImage(BaseModel):
    id: str
    store_product_image_url: str

    model_config = ConfigDict(from_attributes=True)
