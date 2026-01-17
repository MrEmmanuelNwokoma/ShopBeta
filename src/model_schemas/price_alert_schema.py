from pydantic import BaseModel
from src.model_schemas.store_product import ReadStoreProduct



class BasePriceAlert(BaseModel):
    target_price: str



class CreatePriceAlert(BasePriceAlert):
    store_product_id: str
    


class ReadPriceAlert(BasePriceAlert):
    price_alert_id: str
    store_product: ReadStoreProduct



class UpdatePriceAlert(BasePriceAlert):
    store_product_id: str