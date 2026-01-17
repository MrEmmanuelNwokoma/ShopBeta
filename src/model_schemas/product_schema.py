from pydantic import BaseModel, HttpUrl



class BaseProduct(BaseModel):
    name: str
    brand: str
    description: str
    product_url: HttpUrl

class CreateProduct(BaseProduct):
    pass

class ReadProduct(BaseProduct):
    id: str

class UpdateProduct(BaseProduct):
    pass
