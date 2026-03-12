"""
Pydantic schemas for validation
"""
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from datetime import datetime
from src.enums.enums import UserRole




class BaseUserSchema(BaseModel):
    """Base user schema"""
    
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    """Schema for creating user"""
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: UserRole = UserRole.ADMIN

class LoginUser(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone number must be provided")
        return self

class UserProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    role: UserRole
    is_email_verified: bool 
    # is_super_admin: bool 
    last_login: datetime | None = None


    model_config = ConfigDict(from_attributes=True)

class ReadUser(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseUserSchema):
    """Schema for updating user"""
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None= None
    location: str | None= None

