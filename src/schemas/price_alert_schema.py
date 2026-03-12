"""
Pydantic schema for validation
"""
from pydantic import BaseModel
from src.model_schemas.store_product import ReadStoreProduct



class BasePriceAlert(BaseModel):
    """Parent store schema which other store schemas inherit"""
    target_price: str



class CreatePriceAlert(BasePriceAlert):
    """Schema for creating a price_alert"""
    store_product_id: str
    


class ReadPriceAlert(BasePriceAlert):
    """Schema for reading price_alert"""
    price_alert_id: str
    store_product: ReadStoreProduct



class UpdatePriceAlert(BasePriceAlert):
    """Schema for updating price_alert"""
    store_product_id: str