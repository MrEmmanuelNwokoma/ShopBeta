from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_price_history_service
from src.services.price_history_service import PriceHistoryService

price_history_router = APIRouter(prefix="/api/v1/price_history", tags=["Price History"])

@price_history_router.get("/{store_product_id}")
async def get_store_product_price_history(
    store_product_id: str,
    price_history_service: PriceHistoryService = Depends(get_price_history_service)
):
    response = await price_history_service.get_store_product_price_history(store_product_id)
    return response
