import pytest
from sqlalchemy import select
from models.users_model import User

from enums.user_enums import UserRole
@pytest.mark.asyncio
async def test_register_user(client, db):
    response = await client.post(
        "/register",
        json={
            "name": "test",
            "password": "test1"
        }
    )

    assert response.status_code== 200

    result = await db.execute(
        select(User).where(User.name == "test")
    )

    user = result.scalar_one_or_none()

    assert user is not None

@pytest.mark.asyncio
async def  test_duplicate_name(client):
        response = await client.post(
        "/register",
        json={
            "name":"test" ,
            "password": "test1"
        }
    )

        assert response.status_code== 200
        response = await client.post(
        "/register",
        json={
            "name":"test" ,
            "password": "test1"
        }
    )
        assert response.status_code == 409


@pytest.mark.asyncio
async def  test_user_login(client):
        response = await client.post(
        "/register",
        json={
            "name":"test" ,
            "password": "test1"
        }
    )
        response = await client.post(
        "/login",
        data={
            "username":"test" ,
            "password": "test1"
        }
    )
        data=response.json()
        assert "access_token" in data
        assert data["token_type"]=="bearer"
        assert response.status_code==200
@pytest.mark.asyncio
async def test_wrong_user_name_login(client):
        response = await client.post(
        "/register",
        json={
            "name":"test" ,
            "password": "test1"
        }
    )
        response = await client.post(
        "/login",
        data={
            "username":"ben" ,
            "password": "test1"
        }
    )
        assert response.status_code==401


@pytest.mark.asyncio
async def test_wrong_password_login(client):
        response = await client.post(
        "/register",
        json={
            "name":"test" ,
            "password": "test1"
        }
    )
        response = await client.post(
        "/login",
        data={
            "username":"test" ,
            "password": "ben"
        }
    )
        assert response.status_code==401


import pytest
from sqlalchemy import select
from models.users_model import User
from enums.user_enums import UserRole


@pytest.mark.asyncio
async def test_deactivated_user_login(client, db):


    response = await client.post(
        "/register",
        json={
            "name": "admin",
            "password": "admin1"
        }
    )

    result = await db.execute(
        select(User).where(User.name == "admin")
    )
    admin = result.scalar_one_or_none()
    admin.role = UserRole.ADMIN
    await db.commit()

    response = await client.post(
        "/register",
        json={
            "name": "test",
            "password": "test1"
        }
    )

    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    response = await client.patch(
        "/user/deactivate",
        params={
            "name": "test"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    response = await client.post(
        "/login",
        data={
            "username": "test",
            "password": "test1"
        }
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_all_users(client, db):

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
    admin = result.scalar_one_or_none()
    admin.role = UserRole.ADMIN
    await db.commit()

    # Create normal user
    await client.post(
        "/register",
        json={
            "name": "test",
            "password": "test1"
        }
    )

    # Login as admin
    response = await client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin1"
        }
    )

    token = response.json()["access_token"]

    # Delete all users
    response = await client.delete(
        "/delete",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    # Verify users were deleted
    result = await db.execute(
        select(User).where(User.name == "test")
    )

    user = result.scalar_one_or_none()

    assert user is None

@pytest.mark.asyncio
async def test_admin_can_update_role(client, db):

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

    await client.post(
        "/register",
        json={"name": "test", "password": "test1"}
    )

    response = await client.post(
        "/login",
        data={"username": "admin", "password": "admin1"}
    )

    token = response.json()["access_token"]

    response = await client.patch(
        "/user",
        json={
            "name": "test",
            "role": "admin"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

@pytest.mark.asyncio
async def test_member_cannot_update_role(client):

    await client.post(
        "/register",
        json={"name": "member", "password": "member1"}
    )

    response = await client.post(
        "/login",
        data={"username": "member", "password": "member1"}
    )

    token = response.json()["access_token"]

    response = await client.patch(
        "/user",
        json={
            "name": "member",
            "role": "admin"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403