from dotenv import load_dotenv
import os
from google import genai
from openrouter import OpenRouter
import os
load_dotenv()
api_key=os.getenv("GIMINI_API_KEY")
client=genai.Client(api_key=api_key)
async def get_recommendation_gemini(user_preference:str):

    interaction=await client.aio.interactions.create(
        model="gemini-3.8-flash",
        input=user_preference
    )

    return {"response":interaction.output_text}



client_openrouter = OpenRouter(api_key=os.getenv("OPEN_ROUTER_API_KEY"))


async def recommend_open_router(user_preference:str):
    response = await client_openrouter.chat.send_async(
        model="openrouter/free",
        messages=[
            {
                "role": "user", 
                "content": user_preference
            }
        ]
    )
    return {"response":response.choices[0].message.content}

