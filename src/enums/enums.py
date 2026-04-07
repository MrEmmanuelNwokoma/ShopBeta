from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    GUEST_USER = "guest_user"

class Categories(str, Enum):
    SMART_PHONE =  "smart_phone"
    LAPTOP = "laptop"
    

class NotificationType(str, Enum):
    PRICE_DROP = "price_drop"
    PRICE_INCREASE = "price_increase"
    PRICE_CHANGE = "price_change"
    ALERT_CREATED = "alert_created"
    ALERT_TRIGGERED = "alert_triggered"
    SYSTEM = "system"


class EventType(str, Enum):
    USER_CREATED = "user_created"
    PRICE_ALERT_TRIGGERED = "price_alert_triggered"
    DOMAIN_EVENT = "domain_event"
    