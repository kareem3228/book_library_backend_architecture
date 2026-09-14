from pydantic import BaseModel
from datetime import datetime,timezone,UTC
class CreateRental(BaseModel):
    book_id:int


class RentalSummery(BaseModel):
    id:int
    user_id:int
    book_id:int
    rented_at:datetime
    returned_at:datetime|None

    model_config={

        "from_attributes":True
    }