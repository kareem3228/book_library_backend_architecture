from database import Base
from sqlalchemy import Integer,Column,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship


class Rental(Base):
    __tablename__="rentals"
    id=Column(Integer,primary_key=True)
    rented_at=Column(DateTime(timezone=True),server_default=func.now())
    returned_at=Column(DateTime(timezone=True),nullable=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    book_id=Column(Integer,ForeignKey("books.id",ondelete="CASCADE"),nullable=False)
    user=relationship("User",back_populates="rentals")
    book=relationship("Book",back_populates="rentals")
    
    
