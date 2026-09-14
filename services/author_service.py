from sqlalchemy.ext.asyncio import AsyncSession
from schemas.author_schema import AuthorCreate,AuthorUpdate
from models.authors import Author
from models.books import Book
from sqlalchemy import select,delete
from fastapi import HTTPException
async def create_author(session:AsyncSession,author_create:AuthorCreate):
    author=Author(name=author_create.name)
    session.add(author)
    await session.commit()
    return author

async def find_author(session:AsyncSession,id:int):
    stmnt=select(Author).where(Author.id==id)
    result=await session.execute(stmnt)
    author=result.scalar()
    if author is None:
        raise HTTPException(status_code=404,detail="author not found")
    return author
    
async def update_author(session:AsyncSession,id:int,author_update:AuthorUpdate):
    stmnt=select(Author).where(Author.id==id)
    result=await session.execute(stmnt)
    author=result.scalar()
    if author is None:
        raise HTTPException(status_code=404,detail="author not found")
    author.name=author_update.name
    await session.commit()
    return author

async def delete_author(session:AsyncSession,id:int):
    stmnt=select(Author).where(Author.id==id)
    result=await session.execute(stmnt)
    author=result.scalar()
    if author is None:
        raise HTTPException(status_code=404,detail="author not found")
    await session.delete(author)
    await session.commit()

async def find_all_author(session:AsyncSession):
    stmt=select(Author)
    result=await session.execute(stmt)
    authors=result.scalars().all()
    if not authors:
        raise HTTPException(status_code=404,detail="no authors found")
    return authors

async def delete_all_authors(session:AsyncSession):
    stmnt=delete(Author)
    await session.execute(stmnt)
    await session.commit()

async def deactivate_author(author_id:int,session:AsyncSession):
    result=await session.execute(select(Author).where(Author.id==author_id))
    author=result.scalar_one_or_none()
    if author is None:
        raise HTTPException(status_code=404,detail="no author found")
    if author.is_active==False:
        raise HTTPException(status_code=409,detail="author already deactivated")
    author.is_active=False
    await session.commit()
