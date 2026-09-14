# tests/factories.py

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from authentication.pwd import hash_password
from enums.user_enums import UserRole
from models.users_model import User
from models.authors import Author
from models.books import Book
from models.rental import Rental


async def create_admin(db: AsyncSession):
    admin = User(
        name="admin",
        password_hash=hash_password("admin1"),
        role=UserRole.ADMIN,
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    return admin


async def create_member(db: AsyncSession,name="member"):
    member = User(
        name=name,
        password_hash=hash_password("member1"),
        role=UserRole.MEMBER,
    )

    db.add(member)
    await db.commit()
    await db.refresh(member)

    return member


async def create_author(db: AsyncSession, name="Test Author"):
    author = Author(
        name=name
    )

    db.add(author)
    await db.commit()
    await db.refresh(author)

    return author


async def create_book(
    db: AsyncSession,
    author=None,
    title="Test Book",
    year=None,
    genre="Test Genre"
):
    if author is None:
        author = await create_author(db)

    book = Book(
        title=title,
        author=author,
        year=year or datetime.now(),
        genre=genre,
    )

    db.add(book)
    await db.commit()
    await db.refresh(book)

    return book


async def create_rental(
    db: AsyncSession,
    user=None,
    book=None
):
    if user is None:
        user = await create_member(db)

    if book is None:
        book = await create_book(db)

    rental = Rental(
        user=user,
        book=book,
    )

    db.add(rental)
    await db.commit()
    await db.refresh(rental)

    return rental