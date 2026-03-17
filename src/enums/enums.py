from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    GUEST_USER = "guest_user"

class Categories(str, Enum):
    SMART_PHONE =  "smart_phone"
    LAPTOP = "laptop"
    
    