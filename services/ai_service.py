from dotenv import load_dotenv
import os
from google import genai
from openrouter import OpenRouter
import os
from schemas.ai_schema import AiResponse
from prompts.book_recommendation import BOOK_RECOMMENDATION_PROMPT
load_dotenv()
api_key=os.getenv("GIMINI_API_KEY")
client=genai.Client(api_key=api_key)
async def get_recommendation_gemini(user_preference:str):

    interaction=await client.aio.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction=BOOK_RECOMMENDATION_PROMPT,
        input=user_preference,
        response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": AiResponse.model_json_schema()
        }
    )

    return AiResponse.model_validate_json(interaction.output_text)




client_openrouter = OpenRouter(api_key=os.getenv("OPEN_ROUTER_API_KEY"))

async def recommend_open_router(user_preference: str):
    response = await client_openrouter.chat.send_async(
        model="openrouter/free",
        messages=[

            {
                "role": "system", 
                "content": BOOK_RECOMMENDATION_PROMPT
            },
            
            {
                "role": "user", 
                "content": user_preference
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "your_custom_output",
                "strict": True,
                "schema": AiResponse.model_json_schema() 
            }
        }

    )
    
    return AiResponse.model_validate_json(response.choices[0].message.content)