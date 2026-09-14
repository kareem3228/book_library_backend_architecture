from fastapi import FastAPI
from routers.author_router import router as author_router
from routers.books_router import router as books_router
from routers.auth_router import router as auth_router
from routers.rental_router import router as rental_router
from contextlib import asynccontextmanager
from database import engine,Base

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app=FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(author_router)
app.include_router(books_router)
app.include_router(rental_router)