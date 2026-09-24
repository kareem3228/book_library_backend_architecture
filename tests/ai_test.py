import pytest
from tests.factory import create_member,create_book
@pytest.mark.asyncio
async def test_ai_assistant_gemini_recommendation(client,db):
    await create_member(db=db)
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token=response.json()["access_token"]
    async with client.stream(
        "post",
        "/library_assistant/ai/gemini",
        json={"preference":"recommend me a harry potter book"},
        headers={
            "Authorization":f"Bearer {token}"
        }
    )as response:
        assert response.status_code==200
        chunks=""
        async for chunk in response.aiter_text():
            chunks+=chunk
    assert chunks !=""

@pytest.mark.asyncio
async def test_ai_assistant_gemini_test_tool(client,db):
    await create_member(db=db)
    await create_book(db=db)
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token=response.json()["access_token"]
    async with client.stream(
        "post",
        "/library_assistant/ai/gemini",
        json={"preference":"find me a book called test book"},
        headers={
            "Authorization":f"Bearer {token}"
        }
    )as response:
        assert response.status_code==200
        chunks=""
        async for chunk in response.aiter_text():
            chunks+=chunk
    assert chunks !=""


@pytest.mark.asyncio
async def test_ai_assistant_gemini_no_book_found(client,db):
    await create_member(db=db)
    await create_book(db=db)
    response = await client.post(
        "/login",
        data={
            "username": "member",
            "password": "member1"
        }
    )
    token=response.json()["access_token"]
    async with client.stream(
        "post",
        "/library_assistant/ai/gemini",
        json={"preference":"find me a book called twighlight"},
        headers={
            "Authorization":f"Bearer {token}"
        }
    )as response:
        assert response.status_code==404
