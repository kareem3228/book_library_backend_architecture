from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from authentication.jwt import verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select
from models.users_model import User
from fastapi import HTTPException
from schemas.user_schema import TokenData
from enums.user_enums import UserRole
oauth2scheme=OAuth2PasswordBearer("/login")
async def get_current_user(
        token:str=Depends(oauth2scheme),
        session: AsyncSession= Depends(get_db)
):
    payload=verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401,detail="no payload") 
    user_id=payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401,detail="no user-id")
    try:
        token_data=TokenData(user_id=int(user_id))
    except ValueError:
        raise HTTPException(status_code=401,detail="invalid-value")
    result=await session.execute(select(User).where(User.id==token_data.user_id))
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401,detail="no user")
    if user.is_active is False:
        raise HTTPException(status_code=401,detail="user is deactivated")
    return user


async def require_admin(current_user: User=Depends(get_current_user)):
    if current_user.role!=UserRole.ADMIN:
        raise HTTPException(status_code=403,detail="not enough permissions")
    return current_user


        
