from pydantic import BaseModel, HttpUrl
from src.model_schemas.product_schema import ReadProduct
from src.model_schemas.store_schema import ReadStore


class BaseStoreProduct(BaseModel):
    price: str
    instock: str


class ReadStoreProduct(BaseStoreProduct):
    store: ReadStore
    product: ReadProduct

class CreateStoreProduct(BaseStoreProduct):
    store_id: str
    product_id: str