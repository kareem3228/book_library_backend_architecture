import pytest

from models.rental import Rental
from tests.factory import create_member, create_book, create_rental


@pytest.mark.asyncio
async def test_user_can_rent_book(client, db):
    user = await create_member(db)
    book = await create_book(db)

    # We need the authenticated user's token.
    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.post(
        "/rental",
        json={"book_id": book.id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == user.id
    assert response.json()["book_id"] == book.id
    assert response.json()["returned_at"] is None


@pytest.mark.asyncio
async def test_cannot_rent_already_rented_book(client, db):
    user = await create_member(db)
    book = await create_book(db)
    await create_rental(db, user=user, book=book)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.post(
        "/rental",
        json={"book_id": book.id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_cannot_rent_nonexistent_book(client, db):
    await create_member(db)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.post(
        "/rental",
        json={"book_id": 999999},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_can_return_rental(client, db):
    user = await create_member(db)
    book = await create_book(db)
    rental = await create_rental(db, user=user, book=book)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.patch(
        f"/rental/{rental.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["returned_at"] is not None


@pytest.mark.asyncio
async def test_cannot_return_nonexistent_rental(client, db):
    await create_member(db)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.patch(
        "/rental/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_return_another_users_rental(client, db):
    user1 = await create_member(db)
    user2 = await create_member(db, name="member2")

    book = await create_book(db)
    rental = await create_rental(db, user=user2, book=book)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.patch(
        f"/rental/{rental.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cannot_return_already_returned_rental(client, db):
    user = await create_member(db)
    book = await create_book(db)
    rental = await create_rental(db, user=user, book=book)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    first_response = await client.patch(
        f"/rental/{rental.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert first_response.status_code == 200

    second_response = await client.patch(
        f"/rental/{rental.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_user_can_get_rentals(client, db):
    user = await create_member(db)
    book1 = await create_book(db)
    book2 = await create_book(db, title="Second Book")

    await create_rental(db, user=user, book=book1)
    await create_rental(db, user=user, book=book2)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.get(
        "/rental",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_rentals_when_user_has_none(client, db):
    await create_member(db)

    login = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = login.json()["access_token"]

    response = await client.get(
        "/rental",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404