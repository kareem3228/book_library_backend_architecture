import pytest
from sqlalchemy import select

from models.books import Book
from tests.factory import (
    create_admin,
    create_member,
    create_author,
    create_book,
)


@pytest.mark.asyncio
async def test_admin_can_create_book(client, db):
    await create_admin(db)
    author = await create_author(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.post(
        f"/authors/{author.id}/books",
        json={
            "title": "Test Book",
            "year": "2025-01-01T00:00:00",
            "genre": "Fiction"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_member_cannot_create_book(client, db):
    await create_member(db)
    author = await create_author(db)

    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token = response.json()["access_token"]

    response = await client.post(
        f"/authors/{author.id}/books",
        json={
            "title": "Test Book",
            "year": "2025-01-01T00:00:00",
            "genre": "Fiction"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_get_book(client, db):
    await create_admin(db)
    book = await create_book(db)

    response = await client.get(f"/books/{book.id}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_nonexistent_book(client):
    response = await client.get("/books/999999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_update_book(client, db):
    await create_admin(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        f"/books/{book.id}",
        json={
            "title": "Updated Book"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_member_cannot_update_book(client, db):
    await create_member(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        f"/books/{book.id}",
        json={
            "title": "Updated Book"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_update_nonexistent_book(client, db):
    await create_admin(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        "/books/999999",
        json={
            "title": "Updated Book"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_delete_book(client, db):
    await create_admin(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.delete(
        f"/books/{book.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    result = await db.execute(
        select(Book).where(Book.id == book.id)
    )

    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_member_cannot_delete_book(client, db):
    await create_member(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token = response.json()["access_token"]

    response = await client.delete(
        f"/books/{book.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_delete_nonexistent_book(client, db):
    await create_admin(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.delete(
        "/books/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_delete_all_books(client, db):
    await create_admin(db)
    await create_book(db)
    await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.delete(
        "/books",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    result = await db.execute(select(Book))
    books = result.scalars().all()

    assert books == []


@pytest.mark.asyncio
async def test_member_cannot_delete_all_books(client, db):
    await create_member(db)
    await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token = response.json()["access_token"]

    response = await client.delete(
        "/books",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_author_books(client, db):
    author = await create_author(db)
    await create_book(db, author=author)
    await create_book(db, author=author)

    response = await client.get(
        f"/authors/{author.id}/books"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_books_for_nonexistent_author(client):
    response = await client.get(
        "/authors/999999/books"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_books(client, db):
    await create_book(db)
    await create_book(db)

    response = await client.get("/books")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_all_books_when_empty(client):
    response = await client.get("/books")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_deactivate_book(client, db):
    await create_admin(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        f"/book/{book.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    await db.refresh(book)

    assert book.is_active is False


@pytest.mark.asyncio
async def test_member_cannot_deactivate_book(client, db):
    await create_member(db)
    book = await create_book(db)

    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        f"/book/{book.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_deactivate_nonexistent_book(client, db):
    await create_admin(db)

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )
    token = response.json()["access_token"]

    response = await client.patch(
        "/book/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_find_book_name(client,db):
    book=await create_book(db)
    book2=await create_book(db)
    response = await client.get(
        "/book/name",
        params={"name": "Test Book"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_find_book_name_case_sensetive(client,db):
    book=await create_book(db)
    response = await client.get(
        "/book/name",
        params={"name": "test book"}
    )
    data=response.json()
    assert data[0]["title"]=='Test Book'
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_find_book_name_not_complete(client,db):
    book=await create_book(db)
    response = await client.get(
        "/book/name",
        params={"name": "test"}
    )
    data=response.json()
    assert data[0]["title"]=='Test Book'
    assert response.status_code == 200
@pytest.mark.asyncio
async def test_find_wrong_book_name(client,db):
    book=await create_book(db)
    response = await client.get(
        "/book/name",
        params={"name": "balls"}
    )
    data=response.json()
    assert response.status_code == 404