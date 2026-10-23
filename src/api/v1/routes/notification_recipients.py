from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_notification_recipient_service
from src.services.notification_recipients import NotificationRecipientService
from src.models.user import User




notification_recipient_router = APIRouter(prefix="/api/v1/notification_recipients", tags=["Notification_recipients"])





@notification_recipient_router.get("/{notification_recipient_id}")
async def get_user_notification(
    notification_recipient_id: str,
    notification_recipient_service: NotificationRecipientService = Depends(get_notification_recipient_service)
):
    response = await notification_recipient_service.get_user_notification(notification_recipient_id)
    return response

@notification_recipient_router.put("/{notification_recipient_id}/mark_as_read")
async def mark_notification_as_read(
    notification_recipient_id: str,
    current_user: User = Depends(get_current_user),
    notification_recipient_service: NotificationRecipientService = Depends(get_notification_recipient_service)
):
    response = await notification_recipient_service.mark_as_read(notification_recipient_id, current_user.id)
    return response


@notification_recipient_router.get("/")
async def get_user_notifications(
    current_user: User = Depends(get_current_user),
    notification_recipient_service: NotificationRecipientService = Depends(get_notification_recipient_service)
):
    response = await notification_recipient_service.get_user_notifications(current_user.id)
    return response