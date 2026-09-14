from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas.user_schema import CreateUser, LoginUser
from services.user_service import create_user, login_user,delete_user,deactivate_user,change_role
from schemas.user_schema import Token,roleupdate
from models.users_model import User
from authentication.dependencies import require_admin
router = APIRouter()


@router.post("/register")
async def register_user(
    data: CreateUser,
    session: AsyncSession = Depends(get_db)
):
    return await create_user(session, data)


@router.post("/login",response_model=Token)
async def login_user_endpoint(
    form_data:OAuth2PasswordRequestForm= Depends(),
    session: AsyncSession = Depends(get_db)
):
    data=LoginUser(name=form_data.username,
                  password=form_data.password )
    return await login_user(session, data)

@router.delete("/delete",status_code=204)
async def delete_all_users_endpoint(session:AsyncSession=Depends(get_db),admin:User=Depends(require_admin)):
    await delete_user(session=session)

@router.patch("/user/deactivate",status_code=200)
async def deactivate_user_endpoint(name:str,admin:User=Depends(require_admin), session:AsyncSession=Depends(get_db)):
    return await deactivate_user(name=name,session=session)

@router.patch("/user",status_code=204)
async def change_role_endpoint(data:roleupdate,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    await change_role(data=data,session=session)