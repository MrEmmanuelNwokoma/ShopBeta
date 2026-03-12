from src.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from pydantic import EmailStr


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_all_users(self):
        """to fetch all users from database"""
        users = self.get_all()
        return users

    async def get_user_by_email(self, email: EmailStr):
        result = await self.session.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()

    async def deactivate_user(self, user_id: str):
        """soft delete a user"""
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.delete(user_id, soft=True)
        return True

    async def restore_user(self, user_id: str):
        """Restore a soft-deleted user."""
        user = await self.get_by_id(user_id)
        if not user or not hasattr(user, "is_deleted"):
            return False

        user.is_deleted = False
        return True

    async def get_user_by_phone_number(self, phone_number: str):
        result = await self.session.execute(select(self.model).where(self.model.phone_number == phone_number))
        return result.scalar_one_or_none()

    # async def get_super_admin(self):
    #     result = await self.session.execute(select(User).where(User.is_super_admin == True))
    #     return result.scalar_one_or_none()

    async def verify_token(self, token: str):
        result = await self.session.execute(select(User).where(User.verification_token == token))
        return result.scalar_one_or_none()
