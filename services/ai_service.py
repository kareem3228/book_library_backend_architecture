from dotenv import load_dotenv
import os
from google import genai
from openrouter import OpenRouter
import json
import os
from schemas.ai_schema import AiResponse
from prompts.book_recommendation import BOOK_ASSISTANT_PROMPT
from tools.book_definitions import search_books_tool_gimini
from tools.book_tools import search_books
from sqlalchemy.ext.asyncio import AsyncSession
load_dotenv()
api_key=os.getenv("GIMINI_API_KEY")
client=genai.Client(api_key=api_key)
async def get_assistance_gemini(user_preference:str,session:AsyncSession):

    interaction=await client.aio.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction=BOOK_ASSISTANT_PROMPT,
        input=user_preference,
        response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": AiResponse.model_json_schema()
        },
        tools=[search_books_tool_gimini]
    )
    tool_call = next((
    step for step in interaction.steps
    if step.type == "function_call"
    ),None)
    print([step.type for step in interaction.steps])
    if tool_call:
        if tool_call.name=="search_books":
            result = await search_books(name=tool_call.arguments["name"],session=session)
        interaction=await client.aio.interactions.create(
            model="gemini-3.5-flash-lite",
            system_instruction=BOOK_ASSISTANT_PROMPT,
            previous_interaction_id=interaction.id,
            input=[
            {
                "type": "function_result",
                "name": tool_call.name,
                "call_id": tool_call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    }
                ]
            }
            ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": AiResponse.model_json_schema()
            }
        )

    return AiResponse.model_validate_json(interaction.output_text)


