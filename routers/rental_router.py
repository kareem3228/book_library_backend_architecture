from fastapi import APIRouter
from schemas.rental_schema import CreateRental,RentalSummery
from authentication.dependencies import get_current_user
from models.users_model import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.rental_service import rent_book,return_rental,get_userrental
from database import get_db
router=APIRouter()

@router.post("/rental",status_code=201,response_model=RentalSummery)
async def rent_book_endpoint(data:CreateRental,user:User=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    return await rent_book(data=data,user_id=user.id,session=session)

@router.patch("/rental/{id}",status_code=200,response_model=RentalSummery)
async def return_rental_endpoint(id:int,user:User=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    return await return_rental(id=id,user_id=user.id,session=session)

@router.get("/rental",status_code=200,response_model=list[RentalSummery])
async def get_userrental_endpoint(user:User=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    return await get_userrental(user_id=user.id,session=session)


