from dotenv import load_dotenv
import json
import os
from schemas.ai_schema import AiResponse
from prompts.book_recommendation import BOOK_ASSISTANT_PROMPT
from tools.book_definitions import search_books_tool_gimini
from tools.book_tools import search_books
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.ai_cost import account_costs
from config.ai_api import client
from config.model_pricing import model_pricing
async def get_assistance_gemini(user_preference:str,session:AsyncSession):

    interaction=await client.aio.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction=BOOK_ASSISTANT_PROMPT,
        input=user_preference,
        stream=True,
        tools=[search_books_tool_gimini]
    )
    tool_call=None
    arguments=""
    interaction_id=None
    input_tokens=None
    output_tokens=None
    mode_pricing_gimini=model_pricing["gemini-3.5-flash-lite"]
    async for event in interaction:
        if event.event_type== "step.start":
            if event.step.type=="function_call":
                tool_call=event.step
        elif event.event_type=="interaction.created":
            interaction_id=event.interaction.id
        elif event.event_type=="step.delta":
            if event.delta.type == "text":
                yield(event.delta.text)
            elif event.delta.type=="arguments_delta":
                arguments+=event.delta.arguments
        elif event.event_type=="interaction.completed":
            input_tokens=event.interaction.usage.total_input_tokens
            output_tokens=event.interaction.usage.total_output_tokens
            total_first_cost=account_costs(input_tokens=input_tokens,output_tokens=output_tokens,input_price=mode_pricing_gimini["input"],output_price=mode_pricing_gimini["output"])
            print(total_first_cost)
            
    if tool_call:
        arguments=json.loads(arguments)
        if tool_call.name=="search_books":
            try:
                result = await search_books(name=arguments["name"],session=session)
            except HTTPException as e:
                yield e.detail
                return
        interaction=await client.aio.interactions.create(
            model="gemini-3.5-flash-lite",
            system_instruction=BOOK_ASSISTANT_PROMPT,
            previous_interaction_id=interaction_id,
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
            stream=True
        )
    second_input_tokens=None
    second_output_tokens=None
    async for event in interaction:
        if event.event_type == "step.delta" and event.delta.type == "text":
            yield(event.delta.text)
        elif event.event_type=="interaction.completed":
            second_input_tokens=event.interaction.usage.total_input_tokens
            second_output_tokens=event.interaction.usage.total_output_tokens
            total_second_cost=account_costs(input_tokens=second_input_tokens,output_tokens=second_output_tokens,input_price=mode_pricing_gimini["input"],output_price=mode_pricing_gimini["output"])
            print(total_second_cost)
            total_cost=total_first_cost+total_second_cost
            print(total_cost)




