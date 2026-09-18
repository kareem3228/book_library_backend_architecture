from pydantic import BaseModel

class UserPrefrence(BaseModel):
    preference:str

class Recommendation(BaseModel):
    title:str
    reason:str
class AiResponse(BaseModel):
    response:list[Recommendation]|None=None
    unrelated_request:str|None=None