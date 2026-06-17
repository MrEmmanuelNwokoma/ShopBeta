from src.events.bus import event_bus
from src.events.notification_event import NotificationCreatedEvent
from src.events.user_events import UserCreatedEvent
from src.events.verification_event import VerificationRequestedEvent
from src.events.handlers.notificaton_handler import handle_notification_created
from src.events.handlers.user_handler import handle_user_created
from src.events.handlers.verification_handler import handle_verification_token_created



def bootstrap_event_initializer():
    event_bus.subscribe(NotificationCreatedEvent, handle_notification_created)
    event_bus.subscribe(UserCreatedEvent, handle_user_created)
    event_bus.subscribe(VerificationRequestedEvent, handle_verification_token_created)
    


    