"""
Pydantic configurations for ShopBeta
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class PydanticConfiguration(BaseSettings):
    """Pydantic confguration for ShopBeta"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY: str
    RESEND_API_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str = "redis://localhost:6379"
    MAIL_FROM: str = "onboarding@resend.dev"
    FIREBASE_CREDENTIALS: str  



config = PydanticConfiguration()