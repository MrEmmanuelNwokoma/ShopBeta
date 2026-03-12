"""
Pydantic configurations for ShopBeta
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class PydanticConfiguration(BaseSettings):
    """Pydantic confguration for ShopBeta"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60



config = PydanticConfiguration()