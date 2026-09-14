from pydantic import BaseModel
from datetime import datetime
class BookCreate(BaseModel):
    title:str
    genre:str
    year:datetime
    
class BookUpdate(BaseModel):
    title:str|None=None
    genre:str|None=None

class BookSummery(BaseModel):
    title:str
    genre:str
    year:datetime
    is_active:bool

    model_config={

        'from_attributes':True
    }

    