from fastapi import APIRouter,Depends
from schemas.book_schema import BookCreate,BookUpdate,BookSummery
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.book_service import create_book,update_book,delete_book,find_book,find_author_books,find_all_books,delete_all_books,deactivate_book
from authentication.dependencies import require_admin,get_current_user
from models.users_model import User
router=APIRouter()

@router.post("/authors/{author_id}/books",status_code=201)
async def create_book_endpoint(data:BookCreate,author_id:int,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    return await create_book(BookCreate=data,session=session,author_id=author_id)

@router.get("/books/{id}",status_code=200,response_model=BookSummery)
async def find_book_endpoint(id:int,session:AsyncSession=Depends(get_db)):
    return await find_book(id=id,session=session)

@router.patch("/books/{id}",status_code=200)
async def update_book_endpoint(id:int,update_book_data:BookUpdate,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    return await update_book(id=id,session=session,BookUpdate=update_book_data)

@router.delete("/books/{id}",status_code=204)
async def delete_book_endpoint(id:int,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    await delete_book(id=id,session=session)

@router.delete("/books",status_code=204)
async def delete_all_books_endpoint(admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    await delete_all_books(session=session)


@router.get("/authors/{author_id}/books",status_code=200,response_model=list[BookSummery])
async def find_authors_books_endpoint(author_id:int,session:AsyncSession=Depends(get_db)):
    return await find_author_books(author_id=author_id,session=session)

@router.get("/books",status_code=200)
async def find_all_nooks_endpoint(session:AsyncSession=Depends(get_db)):
    return await find_all_books(session=session)

@router.patch("/book/{id}",status_code=200)
async def deactivate_book_endpoint(id:int,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    return await deactivate_book(book_id=id,session=session)