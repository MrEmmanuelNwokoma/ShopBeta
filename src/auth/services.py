from datetime import datetime, timezone, timedelta
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from src.models.user import User
from src.schemas.user_schema import CreateUserSchema, ReadUser, LoginUser
from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, EntityNotFound, InvalidResetTokenError
from src.auth.security import verify_password, hash_password
from src.auth.jwt import retrieve_token
from src.auth.schema import TokenResponse
from src.utils.token_utils import TokenUtils
from src.events.user_events import UserCreatedEvent
from src.events.verification_event import VerificationRequestedEvent
from pydantic import EmailStr

class AuthService:
    """Auth services for authentication services"""
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory
        self.token_utils = TokenUtils()
    
    
    async def register_user(self, user_data: CreateUserSchema):
        """Function for creating user"""
        async with self.uow_factory as uow:
            user = await uow.user_repo.get_user_by_email(email=user_data.email)
            if user:
                raise UserAlreadyExistsError(message="Email already exists in database", details={
                    "recommendation": "user should provide a different email"
                })
            data = user_data.model_dump()
            data['password'] = hash_password(user_data.password)
            user = User(**data)
            created_user = await self.uow_factory.user_repo.create(user)
            data = await self.request_verification_token()
            await uow.user_repo.update(id=user.id, data=data)
            await self.uow_factory.collect_event(
                    UserCreatedEvent(
                        first_name=user.first_name, verification_token=data["verification_token"], event_type="NEW_USER_CREATED", email=user.email
                    )
                )
                    
            return ReadUser.model_validate(created_user)

        
        
    async def login(self, login_details: LoginUser):
        """Function for login which supports email and phonenumber"""
        async with self.uow_factory:
            password = login_details.password

            user = None

            if login_details.email:
                user = await self.uow_factory.user_repo.get_user_by_email(login_details.email)
             
            elif login_details.phone_number:
                try:
                    num = phonenumbers.parse(login_details.phone_number, "NG")
                    if phonenumbers.is_valid_number(num):
                        phonenumber = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
                        user = await self.uow_factory.user_repo.get_user_by_phone_number(phonenumber)
                except NumberParseException  as exc:
                    raise InvalidCredentialsError(
                        message="Invalid credentials",
                        details={
                            "recommendaton": "Phone number could not be parsed"
                        }
                    ) from exc
            if not user:
                raise EntityNotFound(
                    message="User not found",
                    details={
                        "recommendation": "Pass the correct credentials"
                    }
                )
            if not verify_password(password, user.password):
                raise InvalidCredentialsError(
                    message="Invalid credentials",
                    details={
                        "recommendation": "Pass the correct password"
                    }
                )
            user.last_login = datetime.now(timezone.utc)
            access_token = retrieve_token(user)
            return TokenResponse(
                access_token = access_token
            )
        
    async def request_verification_token(self):            
        verification_token, expires_at = await self.token_utils.generate_user_verfication_token()
        updated_data = {
            "verification_token": verification_token,
            "verification_token_expires_at": expires_at
        }
        
        return updated_data

    async def resend_verification_token(self, email: EmailStr):
        async with self.uow_factory as uow:
            user = await uow.user_repo.get_user_by_email(email)
            if not user:
                raise EntityNotFound(
                    message="User with the provided email does not exist",
                    details={
                        "recommendations": "Ensure user passes the correct email"
                    })
            data = await self.request_verification_token()
            await uow.user_repo.update(id=user.id, data=data)
            raise uow.collect_event(
                VerificationRequestedEvent(
                first_name=user.first_name, verification_token=data["verification_token"], event_type="NEW_USER_CREATED",
                email=user.email
            )
            )


    async def verify_token(self, token):
       async with self.uow_factory as uow:
            user = await uow.user_repo.verify_token(token)
            if not user:
                raise EntityNotFound(
                    message="User not found",
                    details={
                        "recommendation": "Pass the correct token"
                    }
                )
            expiry_time = user.verification_token_expires_at
            if not expiry_time:
                raise InvalidResetTokenError(
                    message="Invalid token",
                    details={
                        "recommendation": "Pass the correct token"
                    }
                )
            if expiry_time.tzinfo is None:
                expiry_time = expiry_time.replace(tzinfo=timezone.utc)
            
            if expiry_time < datetime.now(timezone.utc):
                raise InvalidResetTokenError(
                    message="Token has expired",
                    details={
                        "recommendation": "Request a new token"
                    }
                )
            user.verification_token = None
            user.verification_token_expires_at = None
            return user
       
    async def verify_user_email(self, token: str):
        async with self.uow_factory:
            verified_user = await self.verify_token(token)
            if not verified_user:
                return False
            verified_user.is_email_verified = True
            return verified_user
       
    async def change_password(self, user_id: str, new_password: str):
        user = await self.uow_factory.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFound(
                message="User not found",
                details={
                    "recommendation": "Pass the correct user_id"
                }
            )

        hashed_password = hash_password(new_password)

        await self.uow_factory.user_repo.update(user_id, data={"password": hashed_password})
        return {
            "status": "success",
            "message": "Your password has been successfully updated."
        }


    
    
