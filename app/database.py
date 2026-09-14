from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from dotenv import load_dotenv
import os
load_dotenv()
class Base(DeclarativeBase):
    pass
database_url=os.getenv('DATABASE_URL')
engine=create_async_engine(database_url)
asyncsessionlocal=async_sessionmaker(bind=engine,expire_on_commit=False)
async def get_db():
    async with asyncsessionlocal() as session:
        yield session