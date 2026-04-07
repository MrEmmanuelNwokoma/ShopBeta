from pydantic import BaseModel, Field
from datetime import datetime, timezone
from src.enums.enums import EventType

class DomainEvent(BaseModel):
    event_id: str
    time_stamp: Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = EventType.DOMAIN_EVENT

    