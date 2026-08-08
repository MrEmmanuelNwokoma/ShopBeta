import secrets
import string
from pydantic import EmailStr
from datetime import datetime, timezone, timedelta
from src.models.user import User
from src.unit_of_work.unit_of_work import UnitOfWork


class TokenUtils:
    

    def generate_token(self, length: int = 6):
        return "".join(secrets.choice(string.digits) for _ in range(length))
    
    async def generate_user_verfication_token(self,  expiry_time: int = 3):
        token = str(self.generate_token())
        expires_at= datetime.now(timezone.utc) + timedelta(minutes=expiry_time)
        
        return token, expires_at
    