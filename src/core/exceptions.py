"""
class exceptions for all ShopBeta exceptions
"""
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ShopBeta(Exception):
    """Base class for all CircleGround exceptions."""
    message: str
    details: Optional[Any] = None

class UserAlreadyExistsError(ShopBeta):
    """Rasied when trying to create a user that already exists."""
    def __init__(self, message="user already exist", details=None):
        super().__init__(message=message, details=details)

    
class EntityNotFound(ShopBeta):
    """Rasied when an entity is not found in dataase"""
    def __init__(self, message="entity not found", details=None):
        super().__init__(message=message, details=details)

class PermissionDenied(ShopBeta):
    """Rasied when an unauthorized user is trying to access information"""
    def __init__(self, message="Permission denied", details=None):
        super().__init__(message=message, details=details)

class StoreAlreadyExistsError(ShopBeta):
    """Raised when store already exist in database"""
    def __init__(self, message="store already exist", details=None):
        super().__init__(message=message, details=details)

     
class InvalidCredentialsError(ShopBeta):
    """Raised when credenetials passed are invalid"""
    def __init__(self, message="Invalid Credentials", details=None):
        super().__init__(message=message, details=details)

class InvalidResetTokenError(ShopBeta):
    def __init__(self, message="Invalid or expired reset token", details=None):
        super().__init__(message=message, details=details)

class DatabaseConnectionError(ShopBeta):
    """Raised when there's a failure when trying to connect to database"""
    def __init__(self, message="failed to connect to database", details=None):
        super().__init__(message=message, details=details)
