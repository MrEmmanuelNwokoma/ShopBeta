from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from src.auth.services import AuthService
from src.services.user_services import UserService
from src.services.store_services import StoreService
from src.services.product_services import ProductService
from src.services.price_history_service import PriceHistoryService
from src.services.store_product_services import StoreProductService
from src.services.price_alert_services import PriceAlertService
from src.services.favorite_services import FavoriteService
from src.services.category_services import CategoryService
from src.auth.jwt import decode_access_token
from src.schemas.user_schema import UserProfile
from src.storage import db
from src.unit_of_work.unit_of_work import UnitOfWork


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session

def get_uow(session: AsyncSession = Depends(get_session)):
    return UnitOfWork(session)

def get_auth_service(uow: UnitOfWork = Depends(get_uow)):
    return AuthService(uow)

def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow)


def get_price_history_service(uow: UnitOfWork = Depends(get_uow)):
    return PriceHistoryService(uow)

def get_price_alert_service(uow: UnitOfWork = Depends(get_uow)):
    return PriceAlertService(uow)


def get_favorite_service(uow: UnitOfWork = Depends(get_uow)):
    return FavoriteService(uow)

def get_category_service(uow: UnitOfWork = Depends(get_uow)):
    return CategoryService(uow)

def get_store_product_service(uow: UnitOfWork = Depends(get_uow)):
    return StoreProductService(
        uow_factory=uow,
        price_alert=get_price_alert_service()
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: UnitOfWork = Depends(get_uow)
)-> UserProfile:
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    payload = decode_access_token(token, credential_exceptions)
    user_id = payload.get("sub")
    if user_id is None:
        raise credential_exceptions
    async with uow:
        user = await uow.user_repo.get_by_id(user_id)
    if not user:
        raise credential_exceptions
    return UserProfile.model_validate(user)
