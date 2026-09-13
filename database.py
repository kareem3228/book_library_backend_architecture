from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
class Base(DeclarativeBase):
    pass
database_url="postgresql+asyncpg://postgres:postgres123@localhost:5432/library_architecture"
engine=create_async_engine(database_url)
asyncsessionlocal=async_sessionmaker(bind=engine,expire_on_commit=False)
async def get_db():
    async with asyncsessionlocal() as session:
        yield session