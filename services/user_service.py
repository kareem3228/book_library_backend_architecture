from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import CreateUser,LoginUser
from models.users_model import User
from sqlalchemy import select
from fastapi import HTTPException
from authentication.pwd import verify_password,hash_password
from authentication.jwt import create_access_token
from schemas.user_schema import Token,roleupdate
from sqlalchemy import delete
from enums.user_enums import UserRole
from sqlalchemy.exc import IntegrityError
async def create_user(session:AsyncSession,data:CreateUser):
    try:
        hashed_password=hash_password(data.password)
        user=User(name=data.name,
                password_hash=hashed_password

        )
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        raise HTTPException(status_code=409,detail="duplicated name")

async def login_user(session:AsyncSession,data:LoginUser):
    result=await session.execute(select(User).where(User.name==data.name))
    user=result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=401,detail="invalid")
    if user.is_active is False:
            raise HTTPException(status_code=401,detail="user is deactivated")
    if not verify_password(Password=data.password,stored_password=user.password_hash):
        raise HTTPException(status_code=401,detail="invalid")
    token=create_access_token(user.id)
    
    return Token(access_token=token,
                 token_type='bearer')

async def delete_user(session:AsyncSession):
    await session.execute(delete(User))
    await session.commit()

async def deactivate_user(name:str,session:AsyncSession):
    result=await session.execute(select(User).where(User.name==name))
    user=result.scalar_one_or_none()
    user.is_active=False
    await session.commit()

async def change_role(data:roleupdate, session:AsyncSession):
     result=await session.execute(select(User).where(User.name==data.name))
     user=result.scalar_one_or_none()
     if user is None:
        raise HTTPException(status_code=404,detail="no user found")
     user.role=data.role
     await session.commit()