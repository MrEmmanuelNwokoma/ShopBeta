from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    GUEST_USER = "guest_user"
    