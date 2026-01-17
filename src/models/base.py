from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import DateTime 

class Base(DeclarativeBase):
    pass

class Basemodel:
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default=lambda: str(uuid4))
    created_at: Mapped[str] = mapped_column(DateTime(timezone), nullable=False,  default=datetime.now(timezone.utc))
    updated_at: Mapped[str] = mapped_column(DateTime(timezone), nullable=False,  default=datetime.now(timezone.utc))
