from fastapi import APIRouter,Depends
from schemas.author_schema import AuthorCreate,AuthorUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.author_service import create_author,update_author,delete_author,find_author,find_all_author,delete_all_authors,deactivate_author
from authentication.dependencies import get_current_user,require_admin
from models.users_model import User
router=APIRouter()

@router.post("/author",status_code=201)
async def create_author_endpoint(data:AuthorCreate,admin:User=Depends(require_admin), session:AsyncSession=Depends(get_db)):
    return await create_author(author_create=data,session=session)

@router.get("/author/{id}",status_code=200)
async def find_author_endpoint(id:int,session:AsyncSession=Depends(get_db)):
    return await find_author(id=id,session=session)

@router.patch("/author/{id}",status_code=200)
async def update_author_endpoint(id:int,author_update_data:AuthorUpdate,admin:User=Depends(require_admin), session:AsyncSession=Depends(get_db)):
    return await update_author(id=id,session=session,author_update=author_update_data)

@router.delete("/author/{id}",status_code=204)
async def delete_author_endpoint(id:int,admin:User=Depends(require_admin), session:AsyncSession=Depends(get_db)):
    await delete_author(id=id,session=session)

@router.delete("/authors",status_code=204)
async def delete_all_authors_endpoint(admin:User=Depends(require_admin), session:AsyncSession=Depends(get_db)):
    await delete_all_authors(session=session)

@router.get("/authors",status_code=200)
async def find_all_authors_endpoint(session:AsyncSession=Depends(get_db)):
    return await find_all_author(session=session)

@router.patch("/author/{id}/deactivate",status_code=200)
async def deactivate_author_endpoint(id:int,admin:User=Depends(require_admin),session:AsyncSession=Depends(get_db)):
    return await deactivate_author(author_id=id,session=session)