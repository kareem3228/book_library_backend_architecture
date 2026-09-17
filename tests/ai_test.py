import pytest
from tests.factory import create_member
@pytest.mark.asyncio
async def test_ai_recommendation_gemini(client,db):
    await create_member(db=db)
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    print(response.status_code)
    print(response.json())
    token=response.json()["access_token"]
    response= await client.post(
        "/recommendation/ai/gemini",
        json={"preference":"recommend me a fantasy book"},
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    data=response.json()
    assert response.status_code==200
    assert data["response"]
@pytest.mark.asyncio
async def test_ai_recommendation_openrouter(client,db):
    await create_member(db=db)
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    print(response.status_code)
    print(response.json())
    token=response.json()["access_token"]
    response= await client.post(
        "/recommendation/ai/openrouter",
        json={"preference":"recommend me a fantasy book"},
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    data=response.json()
    assert response.status_code==200
    assert data["response"]

