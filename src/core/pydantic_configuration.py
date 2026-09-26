"""
Pydantic configurations for ShopBeta
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class PydanticConfiguration(BaseSettings):
    """Pydantic confguration for ShopBeta"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    CHROME_DRIVER: str
    SECRET_KEY: str
    RESEND_API_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str = "redis://localhost:6379"
    MAIL_FROM: str = "onboarding@resend.dev"
    FIREBASE_CREDENTIALS: str
    GEMINI_API_KEY: str
    JUMIA_URL: dict = {
        "Smartphone": "https://www.jumia.com.ng/mobile-phones/",
        "Laptop": "https://www.jumia.com.ng/computing/laptops/",
        "Tablet": "https://www.jumia.com.ng/tablets/",
        "SmartWatch": "https://www.jumia.com.ng/smart-watches/",
        "Headphones": "https://www.jumia.com.ng/electronics-headphone/",
        "Monitor": "https://www.jumia.com.ng/monitors/",
        "Gaming console": "https://www.jumia.com.ng/mlp-video-game-console/",
        "Speakers": "https://www.jumia.com.ng/mlp-speaker/"
    }
    
    SLOT_URL: dict = {
        "Smartphone": "https://slot.ng/categories/phones-and-tablets",
        "Laptop": "https://slot.ng/category/laptops",
        "Tablet": "https://slot.ng/shop?q=tablet",
        "SmartWatch": "https://slot.ng/category/watches",
        "Gaming console": "https://slot.ng/category/Gaming-Gaming",
        "Speakers": "https://slot.ng/category/Home-And-Audio-Speakers",
    }

    KONGA_URL: dict = {
        "Smartphone": "https://www.konga.com/category/phones-tablets-5294",
        "Laptop": "https://www.konga.com/category/laptops-5230",
        "Tablet": "https://www.konga.com/category/tablets-5229",
        "SmartWatch": "https://www.konga.com/category/smartwatches-7576",
        "Headphones": "https://www.konga.com/category/headsets-earphones-5342",
        "Monitor": "https://www.konga.com/category/monitors-5243",
        "Gaming console": "https://www.konga.com/category/games-consoles-1683",
        "Speakers": "https://www.konga.com/category/multimedia-speakers-7809",
    }


config = PydanticConfiguration()
