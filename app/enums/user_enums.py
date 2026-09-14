from enum import Enum
class UserRole(str,Enum):
    MEMBER="member"
    ADMIN="admin"