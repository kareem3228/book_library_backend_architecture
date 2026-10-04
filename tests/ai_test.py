import pytest
from tests.factory import create_member,create_book
from unittest.mock import AsyncMock, patch
from services.ai_interaction import get_interaction
from google.genai._gaos.lib.compat_errors import (APITimeoutError,NotFoundError)
from config.ai_api import client
from google.genai import errors
gemini_client=client
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
async def test_ai_assistant_gemini_retryable_timout_error(client,db):
    await create_book(db=db)
    successfull_interaction=object()
    mock_test=AsyncMock()
    mock_test.side_effect=[APITimeoutError("timeout"),APITimeoutError("timeout"),successfull_interaction]
    with patch.object(gemini_client.aio.interactions,"create",mock_test):
            result=await get_interaction(user_preference="find me a book called test book",model="gemini-3.5-flash-lite",fallback_model="gemini-3.1-flash-lite")
            interaction,model=result
            assert mock_test.call_count == 3
            assert interaction==successfull_interaction

@pytest.mark.asyncio
async def test_ai_assistant_gemini_main_model(client,db):
            await create_book(db=db)
            result=await get_interaction(user_preference="find me a book called test book",model="gemini-3.5-flash-lite",fallback_model="gemini-3.1-flash-lite")
            interaction,model=result
            assert model=="gemini-3.5-flash-lite"


@pytest.mark.asyncio
async def test_ai_assistant_gemini_fall_back_model(client,db):
            await create_book(db=db)
  
            result=await get_interaction(user_preference="find me a book called test book",model="incorrectmodel",fallback_model="gemini-3.1-flash-lite")
            interaction,model=result
            assert model=="gemini-3.1-flash-lite"



@pytest.mark.asyncio
async def test_ai_assistant_gemini_non_retrayble_error(client,db):
    await create_book(db=db)
    
    mock_test=AsyncMock()
    mock_test.side_effect=[errors.APIError(
    400,
    {"message": "bad request"}
)]
    with patch.object(gemini_client.aio.interactions,"create",mock_test):
            result=await get_interaction(user_preference="find me a book called test book",model="gemini-3.5-flash-lite",fallback_model="gemini-3.1-flash-lite")
            assert mock_test.call_count == 1
            assert result==None



@pytest.mark.asyncio
async def test_ai_assistant_gemini_incorrect_model(client,db):
            await create_book(db=db)
            result=await get_interaction(user_preference="find me a book called test book",model="incorrect model",fallback_model="incorrect model")
            assert result==None


@pytest.mark.asyncio
async def test_ai_assistant_gemini_retryable_timout_error_fail(client,db):
    await create_book(db=db)
    mock_test=AsyncMock()
    mock_test.side_effect=[APITimeoutError("timeout"),APITimeoutError("timeout"),APITimeoutError("timeout"),APITimeoutError("timeout"),APITimeoutError("timeout"),APITimeoutError("timeout")]
    with patch.object(gemini_client.aio.interactions,"create",mock_test):
            result=await get_interaction(user_preference="find me a book called test book",model="gemini-3.5-flash-lite",fallback_model="gemini-3.1-flash-lite")
            assert mock_test.call_count == 6
            assert result is None
