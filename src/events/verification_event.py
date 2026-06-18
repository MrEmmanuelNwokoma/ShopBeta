from src.events.base import DomainEvent



class VerificationRequestedEvent(DomainEvent):
    first_name: str
    verification_token: str
    email: str

