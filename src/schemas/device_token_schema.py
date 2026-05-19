from pydantic import BaseModel


class AddDeviceToken(BaseModel):
    token: str
    platform: str