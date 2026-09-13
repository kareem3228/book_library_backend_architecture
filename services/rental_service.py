from sqlalchemy.ext.asyncio import AsyncSession
from schemas.rental_schema import CreateRental
from models.rental import Rental
from models.users_model import User
from models.books import Book
from sqlalchemy import select
from fastapi import HTTPException
from datetime import datetime,timezone
async def rent_book(user_id:int,data:CreateRental,session:AsyncSession):
    result=await session.execute(select(Rental).where(Rental.book_id==data.book_id,Rental.returned_at.is_(None)))
    rental=result.scalar_one_or_none()
    if rental: 
        raise HTTPException(
        status_code=409,
        detail="Book is already rented"
        )
    result=await session.execute(select(User).where(User.id==user_id))
    user=result.scalar_one_or_none()
    if user is None: 
        raise HTTPException(status_code=404,detail="not found")
    result=await session.execute(select(Book).where(Book.id==data.book_id))
    book=result.scalar_one_or_none()
    if book is None: 
        raise HTTPException(status_code=404,detail="not found")
    rental=Rental(user_id=user_id,book_id=data.book_id,user=user,book=book)
    session.add(rental)
    await session.commit()
    return rental

async def return_rental(id:int,user_id:int,session:AsyncSession):
    result=await session.execute(select(Rental).where(Rental.user_id==user_id,Rental.id==id))
    rental=result.scalar_one_or_none()
    if rental is None:
        raise HTTPException(status_code=404,detail="not found")
    if rental.returned_at is not None:
        raise HTTPException(status_code=409,detail="book was already returned")
    rental.returned_at=datetime.now(timezone.utc)
    await session.commit()
    return rental

async def get_userrental(user_id:int,session:AsyncSession):
    result=await session.execute(select(Rental).where(Rental.user_id==user_id))
    rentals=result.scalars().all()
    if not rentals:
        raise HTTPException(status_code=404,detail="not found")
    return rentals

