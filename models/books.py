from database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
class Book(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,nullable=False)                                                             
    title=Column(String,nullable=False)
    author_id=Column(Integer,ForeignKey('authors.id',ondelete="CASCADE"),nullable=False)
    year=Column(DateTime(timezone=True),nullable=False)
    author=relationship('Author',back_populates="books")
    genre=Column(String,nullable=True)
    rentals=relationship("Rental",back_populates="book",cascade="all, delete-orphan")
    is_active=Column(Boolean,nullable=False,default=True)