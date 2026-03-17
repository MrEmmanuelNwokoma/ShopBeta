"""
Pydantic schema for validation
"""
from pydantic import BaseModel, ConfigDict
from src.schemas.store_product import ReadStoreProduct



class BasePriceAlert(BaseModel):
    """Parent store schema which other store schemas inherit"""
    target_price: str
    



class PriceAlert(BasePriceAlert):
    """Schema for creating a price_alert"""
    store_product_id: str
    user_id: str
    


class ReadPriceAlert(BasePriceAlert):
    """Schema for reading price_alert"""
    product_name: str
    store_name: str

   
class UpdatePriceAlert(BasePriceAlert):
    """Schema for updating price_alert"""
    store_product_id: str
    user_id: str