from fastapi import APIRouter
from schemas.ai_schema import UserPrefrence,AiResponse
from services.ai_service import get_assistance_gemini
from authentication.dependencies import get_current_user
from models.users_model import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi.responses import StreamingResponse
router=APIRouter()

@router.post("/library_assistant/ai/gemini",status_code=200)
async def get_recommendation_endpoint(preference:UserPrefrence,user:User=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    return StreamingResponse(get_assistance_gemini(user_preference=preference.preference,session=session),media_type="text/plain")


    