# bootstrap_admin.py

import asyncio
from sqlalchemy import select

from database import asyncsessionlocal
from models.users_model import User
from models.rental import Rental
from models.books import Book
from models.authors import Author
from enums.user_enums import UserRole
from authentication.pwd import hash_password


async def create_admin():
    async with asyncsessionlocal() as session:
        result = await session.execute(
            select(User).where(User.name == "admin")
        )

        user = result.scalar_one_or_none()

        if user is not None:
            print("Admin already exists")
            return

        admin = User(
            name="admin",
            password_hash=hash_password("balls"),
            role=UserRole.ADMIN,
            is_active=True
        )

        session.add(admin)
        await session.commit()

        print("Admin created")


asyncio.run(create_admin())