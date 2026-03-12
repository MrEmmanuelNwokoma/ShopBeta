from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Generic, TypeVar, Type
from pydantic import EmailStr
from src.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository for all child repositories"""
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def create(self, obj: ModelType):
        self.session.add(obj)
        return obj
    
    async def get_all(self):
        stmt = select(self.model)

        if hasattr(self.model, "soft_delete"):
            stmt = stmt.where(self.model.soft_delete == False)

        result = await self.session.scalars(stmt)
        return result.all()

    async def get_by_email(self, email: EmailStr):
        result = await self.session.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, id: str):
        result = await self.session.get(self.model, id)
        return result

    async def delete(self, id, soft: bool =False)-> bool:
        obj = await self.get_by_id(id)
        if not obj:
            return False
        
        if soft and hasattr(obj, "is_active"):
            setattr(obj, "is_active", False)
        else:
            await self.session.delete(obj)
        return True
    
    async def update(self, id: str, filters: dict | None = None, data: dict | None = None) -> bool:
            if not data:
                return False

            IGNORE_LIST = [
                'id', 'created_at', 'updated_at'
            ]
            updated_dict = {}
            if data:
                updated_dict = {
                    key: value for key, value in data.items() if key not in IGNORE_LIST
                }

            stmt = update(self.model).values(**updated_dict)
            if id:
                stmt = stmt.where(getattr(self.model, "id") == id)
            elif filters:
                stmt = stmt.filter_by(**filters)
            else:
                raise ValueError(
                    "You must provide either id or filters to update.")

            await self.session.execute(stmt)
            return updated_dict

    
    async def verify_token(self, token: str):
        result = await self.session.execute(select(self.model).where(self.model.verification_token == token))
        return result
    

    async def get_by_phone_number(self, phonenumber: str):
       result = await self.session.execute(select(self.model).where(self.model.phone_number == phonenumber))
       return result.scalar_one_or_none()