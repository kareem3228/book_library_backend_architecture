from fastapi import APIRouter
from schemas.ai_schema import UserPrefrence,AiResponse
from services.ai_service import get_recommendation_gemini,recommend_open_router
from authentication.dependencies import get_current_user
from models.users_model import User
from fastapi import Depends
router=APIRouter()

@router.post("/recommendation/ai/gemini",status_code=200,response_model=AiResponse)
async def get_recommendation_endpoint(preference:UserPrefrence,user:User=Depends(get_current_user)):
    return await get_recommendation_gemini(user_preference=preference.preference)
@router.post("/recommendation/ai/openrouter",status_code=200,response_model=AiResponse)
async def get_recommendation_openrouter_endpoint(preference:UserPrefrence,user:User=Depends(get_current_user)):
    return await recommend_open_router(user_preference=preference.preference)


    