from dotenv import load_dotenv
import json
from tools.book_tools import search_books
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.ai_cost import account_costs
from config.model_pricing import model_pricing
from services.ai_interaction import get_interaction
async def get_assistance_gemini(user_preference:str,session:AsyncSession):
    result=await get_interaction(user_preference=user_preference,model="gemini-3.5-flash-lite",fallback_model="gemini-3.1-flash-lite")
    if result is None:
        yield "AI service is currently unavailable. Please try again later."
        return
    interaction,used_model=result
                

    tool_call=None
    arguments=""
    interaction_id=None
    input_tokens=None
    output_tokens=None
    mode_pricing_gimini=model_pricing[used_model]
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
        elif event.event_type=="error":
            yield "there was an error during the stream"
            return
        elif event.event_type=="interaction.completed":
            input_tokens=event.interaction.usage.total_input_tokens
            output_tokens=event.interaction.usage.total_output_tokens
            total_first_cost=account_costs(input_tokens=input_tokens,output_tokens=output_tokens,input_price=mode_pricing_gimini["input"],output_price=mode_pricing_gimini["output"])
            print(f"total_first_cost: {total_first_cost}")
            
    if tool_call:
        arguments=json.loads(arguments)
        if tool_call.name=="search_books":
            try:
                result = await search_books(name=arguments["name"],session=session)
            except HTTPException as e:
                yield e.detail
                return
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
            ]
        tool_result=await get_interaction(model="gemini-3.5-flash-lite",user_preference=input,fallback_model="gemini-3.1-flash-lite",previous_interaction_id=interaction_id)
        if tool_result is None:
            yield "AI service is currently unavailable. Please try again later."
            return
        interaction,used_model=tool_result
        mode_pricing_gimini=model_pricing[used_model] 
        second_input_tokens=None
        second_output_tokens=None
        async for event in interaction:
            if event.event_type == "step.delta" and event.delta.type == "text":
                yield(event.delta.text)
            elif event.event_type=="error":
                yield "there was an error during the stream"
                return
            elif event.event_type=="interaction.completed":
                second_input_tokens=event.interaction.usage.total_input_tokens
                second_output_tokens=event.interaction.usage.total_output_tokens
                total_second_cost=account_costs(input_tokens=second_input_tokens,output_tokens=second_output_tokens,input_price=mode_pricing_gimini["input"],output_price=mode_pricing_gimini["output"])
                print(total_second_cost)
                total_cost=total_first_cost+total_second_cost
                print(f"total cost:{total_cost}")




