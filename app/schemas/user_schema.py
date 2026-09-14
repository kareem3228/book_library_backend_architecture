from pydantic import BaseModel
from enums.user_enums import UserRole
class CreateUser(BaseModel):
    name:str
    password:str


class LoginUser(BaseModel):
    name:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id:int|None = None

class roleupdate(BaseModel):
    name:str
    role:UserRole