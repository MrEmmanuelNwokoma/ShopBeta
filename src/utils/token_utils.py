import secrets
import string
from datetime import datetime, timezone, timedelta
from src.models.user import User
from src.unit_of_work.unit_of_work import UnitOfWork


class TokenUtils:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    def generate_token(self, length: int = 6):
        return "".join(secrets.choice(string.digits) for _ in range(length))
    
    async def generate_user_verfication_token(self, user: User, expiry_time: int = 3):
        token = self.generate_token()
        user.verification_token  = str(token)
        user.verification_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_time)
        return user.verification_token