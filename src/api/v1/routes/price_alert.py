from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_price_alert_service, get_current_user
from src.services.price_alert_services import PriceAlertService
from src.schemas.price_alert_schema import PriceAlertSchema
from src.models.user import User

price_alert_router = APIRouter(prefix="/api/v1/price_alerts")

@price_alert_router.post("/")
async def create_price_alert(
    price_alert_data: PriceAlertSchema,
    user: User = Depends(get_current_user),
    price_alert_service: PriceAlertService = Depends(get_price_alert_service)
):
    response = await price_alert_service.create_price_alert(price_alert_data=price_alert_data, user_id=user.id)
    return response