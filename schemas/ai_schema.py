from pydantic import BaseModel

class UserPrefrence(BaseModel):
    preference:str

class AiResponse(BaseModel):
    response:str