import os

import httpx
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from database import get_db, Base

load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

test_engine = create_async_engine(
    test_database_url,
    poolclass=NullPool
)

test_async_session = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db():
    async with test_async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()