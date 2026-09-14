from pydantic import BaseModel
class AuthorCreate(BaseModel):
    name:str


class AuthorUpdate(BaseModel):
    name:str
