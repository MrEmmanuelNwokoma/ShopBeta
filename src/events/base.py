from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone
from src.enums.enums import EventType

class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=lambda: uuid4())
    time_stamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = EventType.DOMAIN_EVENT

    