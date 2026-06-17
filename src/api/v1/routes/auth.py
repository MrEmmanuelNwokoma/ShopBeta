from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user_schema import CreateUserSchema, LoginUser
from src.api.v1.dependencies import get_auth_service, get_current_user
from src.models.user import User
from src.auth.services import AuthService
from src.auth.schema import VerificationForm



auth_router = APIRouter(prefix="/api/v1/auth")


@auth_router.post("/")
async def register_guest_user(
    user_data: CreateUserSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    response = await auth_service.register_user(user_data)
    return response


@auth_router.post('/login')
async def login_user(
    login_details: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    username = login_details.username.strip()

    credentials = LoginUser(
        email=username if "@" in username else None,
        phone_number=None if "@" in username else username,
        password=login_details.password
    )

    return await auth_service.login(credentials)

@auth_router.post("/forgot-password")
async def forgot_password(
    email: VerificationForm,
    auth_service: AuthService = Depends(get_auth_service)
):
    response = await auth_service.request_password_reset_token(email.email)
    return response

@auth_router.post("/verify-token")
async def verify_token(
    token: str, 
    auth_service: AuthService = Depends(get_auth_service)
):
    response = await auth_service.verify_token(token)
    return response

@auth_router.post("/verify-email")
async def verify_email(
    token: str,
    auth_service: AuthService = Depends(get_auth_service)

):
    response = await auth_service.verify_user_email(token)
    return response

@auth_router.post("/set-new-password")
async def set_new_password(
    new_password: str,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    response = await auth_service.change_password(user_id=current_user.id, new_password=new_password)
    return response

@auth_router.post("/request-verification-token")
async def request_verification_token(
    email: VerificationForm,
    auth_service: AuthService = Depends(get_auth_service)

):
    response = await auth_service.request_verification_token(email.email)
    return response
    