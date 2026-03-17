from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_price_alert_service
from src.services.price_alert_services import PriceAlertService
from src.schemas.price_alert_schema import CreatePriceAlert

price_alert_router = APIRouter(prefix="/api/v1/price_alerts")

@price_alert_router.post("/")
async def create_price_alert(
    price_alert_data: CreatePriceAlert,
    price_alert_service: PriceAlertService = Depends(get_price_alert_service)
):
    response = await price_alert_service.create_price_alert(price_alert_data)
    return response