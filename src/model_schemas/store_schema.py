from pydantic import BaseModel, HttpUrl


class BaseStore(BaseModel):
    name: str
    website_url: HttpUrl
    is_active: bool = False
    supports_api: bool = False


class CreateStore(BaseStore):
    pass


class ReadStore(BaseStore):
    id: str

class UpdateStore(BaseStore):
    pass



