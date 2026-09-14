import pytest
from sqlalchemy import select
from models.users_model import User
from models.authors import Author
from enums.user_enums import UserRole
@pytest.mark.asyncio
async def test_admin_can_create_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={"name": "admin", "password": "admin1"}
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Login as admin
    response = await client.post(
        "/login",
        data={"username": "admin", "password": "admin1"}
    )

    token = response.json()["access_token"]

    # Create author
    response = await client.post(
        "/author",
        json={
            "name":"ben"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

@pytest.mark.asyncio
async def test_member_cannot_create_author(client):

    await client.post(
        "/register",
        json={"name": "member", "password": "member1"}
    )

    response = await client.post(
        "/login",
        data={"username": "member", "password": "member1"}
    )

    token = response.json()["access_token"]

    response = await client.post(
        "/author",
        json={
            "name":'ben'
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_author(client, db):
    author = Author(name="Test Author")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    response = await client.get(f"/author/{author.id}")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_nonexistent_author(client):
    response = await client.get("/author/999999")

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_admin_can_update_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={"name": "admin", "password": "admin1"}
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Create author
    author = Author(name="Old Name")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as admin
    response = await client.post(
        "/login",
        data={"username": "admin", "password": "admin1"}
    )
    token = response.json()["access_token"]

    # Update author
    response = await client.patch(
        f"/author/{author.id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_member_cannot_update_author(client, db):

    # Create member
    await client.post(
        "/register",
        json={"name": "member", "password": "member1"}
    )

    # Create author directly
    author = Author(name="Old Name")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as member
    response = await client.post(
        "/login",
        data={"username": "member", "password": "member1"}
    )
    token = response.json()["access_token"]

    # Try to update author
    response = await client.patch(
        f"/author/{author.id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_member_cannot_update_author(client, db):

    # Create member
    await client.post(
        "/register",
        json={"name": "member", "password": "member1"}
    )

    # Create author directly
    author = Author(name="Old Name")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as member
    response = await client.post(
        "/login",
        data={"username": "member", "password": "member1"}
    )
    token = response.json()["access_token"]

    # Try to update author
    response = await client.patch(
        f"/author/{author.id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_nonexistent_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={"name": "admin", "password": "admin1"}
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Login as admin
    response = await client.post(
        "/login",
        data={"username": "admin", "password": "admin1"}
    )
    token = response.json()["access_token"]

    # Try to update nonexistent author
    response = await client.patch(
        "/author/999999",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

    # tests/test_authors.py

import pytest
from sqlalchemy import select

from models.users_model import User
from models.authors import Author
from enums.user_enums import UserRole


@pytest.mark.asyncio
async def test_admin_can_delete_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Create author
    author = Author(name="Test Author")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Delete author
    response = await client.delete(
        f"/author/{author.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    # Verify deletion
    result = await db.execute(
        select(Author).where(Author.id == author.id)
    )

    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_member_cannot_delete_author(client, db):

    # Create member
    await client.post(
        "/register",
        json={
            "name": "member",
            "password": "member1"
        }
    )

    # Create author
    author = Author(name="Test Author")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as member
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = response.json()["access_token"]

    # Try to delete author
    response = await client.delete(
        f"/author/{author.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_delete_nonexistent_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Try to delete nonexistent author
    response = await client.delete(
        "/author/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_delete_all_authors(client, db):

    # Create admin
    await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Create authors
    author1 = Author(name="Author 1")
    author2 = Author(name="Author 2")

    db.add_all([author1, author2])
    await db.commit()

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Delete all authors
    response = await client.delete(
        "/authors",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    # Verify deletion
    result = await db.execute(select(Author))
    authors = result.scalars().all()

    assert authors == []


@pytest.mark.asyncio
async def test_member_cannot_delete_all_authors(client, db):

    # Create member
    await client.post(
        "/register",
        json={
            "name": "member",
            "password": "member1"
        }
    )

    # Create author
    await client.post(
        "/register",
        json={
            "name": "another_member",
            "password": "member2"
        }
    )

    author = Author(name="Test Author")
    db.add(author)
    await db.commit()

    # Login as member
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = response.json()["access_token"]

    # Try to delete all authors
    response = await client.delete(
        "/authors",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_authors_when_empty(client):

    response = await client.get("/authors")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_can_deactivate_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Create author
    author = Author(name="Test Author")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Deactivate author
    response = await client.patch(
        f"/author/{author.id}/deactivate",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    await db.refresh(author)

    assert author.is_active is False


@pytest.mark.asyncio
async def test_member_cannot_deactivate_author(client, db):

    # Create member
    await client.post(
        "/register",
        json={
            "name": "member",
            "password": "member1"
        }
    )

    # Create author
    author = Author(name="Test Author")
    db.add(author)
    await db.commit()
    await db.refresh(author)

    # Login as member
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )

    token = response.json()["access_token"]

    # Try to deactivate author
    response = await client.patch(
        f"/author/{author.id}/deactivate",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_deactivate_nonexistent_author(client, db):

    # Create admin
    await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Try to deactivate nonexistent author
    response = await client.patch(
        "/author/999999/deactivate",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404