from services.book_service import find_book_name
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
async def search_books(name:str,session:AsyncSession):
    result=await find_book_name(name=name,session=session)
    return [{"name":book.title ,"genre":book.genre} for book in result]