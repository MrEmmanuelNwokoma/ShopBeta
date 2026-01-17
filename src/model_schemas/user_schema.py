from pydantic import BaseModel, EmailStr




class BaseUserSchema(BaseModel):
    username: str
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    password: str

    
class ReadUser(BaseUserSchema):
    pass


class UpdateUser(BaseUserSchema):
    password: str
