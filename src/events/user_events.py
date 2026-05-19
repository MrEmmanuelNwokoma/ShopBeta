from src.events.base import DomainEvent



class UserCreatedEvent(DomainEvent):
    first_name: str
    verification_token: str
    email: str

