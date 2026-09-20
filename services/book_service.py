from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book_schema import BookCreate,BookUpdate
from models.books import Book
from models.authors import Author
from sqlalchemy import select,delete
from fastapi import HTTPException

async def create_book(session:AsyncSession,BookCreate:BookCreate,author_id:int):
    stmnt=select(Author).where(Author.id==author_id,Author.is_active==True)
    result=await session.execute(stmnt)
    author=result.scalar()
    if author is None:
        raise HTTPException(status_code=404,detail="book not found")
    book=Book(title=BookCreate.title,
              genre=BookCreate.genre,
              year=BookCreate.year,
            author=author)
    session.add(book)
    await session.commit()
    return book

async def find_book(session:AsyncSession,id:int):
    stmnt=select(Book).where(Book.id==id,Book.is_active==True)
    result=await session.execute(stmnt)
    book=result.scalar()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    return book
    
async def update_book(session:AsyncSession,id:int,BookUpdate:BookUpdate):
    stmnt=select(Book).where(Book.id==id)
    result=await session.execute(stmnt)
    book=result.scalar()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    update_data=BookUpdate.model_dump(exclude_unset=True)
    for field,items in update_data.items():
        setattr(book,field,items)
    await session.commit()
    return book

async def delete_book(session:AsyncSession,id:int):
    stmnt=select(Book).where(Book.id==id)
    result=await session.execute(stmnt)
    book=result.scalar()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    await session.delete(book)
    await session.commit()

async def find_author_books(session:AsyncSession,author_id:int):
    stmnt=select(Book).where(Book.author_id==author_id,Book.is_active==True)
    result= await session.execute(stmnt)
    books=result.scalars().all()
    if not books:
        raise HTTPException(status_code=404,detail="no books found")
    return books

async def find_all_books(session:AsyncSession):
    stmt=select(Book).where(Book.is_active==True)
    result=await session.execute(stmt)
    books=result.scalars().all()
    if not books:
        raise HTTPException(status_code=404,detail="no books found")
    return books

async  def delete_all_books(session:AsyncSession):
    stmnt=delete(Book)
    await session.execute(stmnt)
    await session.commit()

async def deactivate_book(book_id:int,session:AsyncSession):
    result=await session.execute(select(Book).where(Book.id==book_id))
    book=result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    if book.is_active== False:
        raise HTTPException(status_code=409,detail='book already deactivated')
    book.is_active=False
    await session.commit()

async def find_book_name(name:str,session:AsyncSession):
    result=await session.execute(select(Book).where(Book.title.ilike(f"%{name}%"),Book.is_active==True))
    books=result.scalars().all()
    if not books:
        raise HTTPException(status_code=404,detail="book not found")
    return books
