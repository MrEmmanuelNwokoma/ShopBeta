from src.schemas.notification import CreateNotification



class AlertNotificationFactory:

    @staticmethod
    def alert_triggered(price_alert_id: str, user_id: str, admin_id: str):
        CreateNotification(
            
        )