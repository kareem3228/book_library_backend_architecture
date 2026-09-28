from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import json
import os
from schemas.ai_schema import AiResponse
from prompts.book_recommendation import BOOK_ASSISTANT_PROMPT
from tools.book_definitions import search_books_tool_gimini
from tools.book_tools import search_books
from fastapi import HTTPException
from services.ai_cost import account_costs
from config.ai_api import client
from config.model_pricing import model_pricing
from google.genai import errors
import httpx
import asyncio
from google.genai._gaos.lib.compat_errors import (APIConnectionError,NotFoundError,APITimeoutError)
async def get_interaction(user_preference:str,fallback_model:str,model:str,previous_interaction_id:str|None=None):
    for attempt in range(3):
        try:
            interaction=await client.aio.interactions.create(
                model=model,
                system_instruction=BOOK_ASSISTANT_PROMPT,
                previous_interaction_id=previous_interaction_id,
                input=user_preference,
                stream=True,
                tools=[search_books_tool_gimini]
            )
            
            return interaction,model
        except NotFoundError:
             break
        except errors.APIError as e:
            if e.code not in [408, 429, 500, 502, 503, 504]:
                return None
            if attempt==2:
                break
            await asyncio.sleep(1)
        except (httpx.TimeoutException,APITimeoutError):
            if attempt==2:
                break
            await asyncio.sleep(1)
        except APIConnectionError:
            if attempt==2:
                return None
            await asyncio.sleep(1)
    for attempt in range(3):  
        try:
                    interaction=await client.aio.interactions.create(
                    model=fallback_model,
                    system_instruction=BOOK_ASSISTANT_PROMPT,
                    input=user_preference,
                    previous_interaction_id=previous_interaction_id,
                    stream=True,
                    tools=[search_books_tool_gimini]
                )
                    return interaction,fallback_model
        except (httpx.TimeoutException, APITimeoutError):
            if attempt == 2:
                return None
            await asyncio.sleep(1)


        except errors.APIError as e:
            if e.code not in [408, 429, 500, 502, 503, 504]:
                return None
            if attempt == 2:
                return None
            await asyncio.sleep(1)

        except NotFoundError:
            return None
