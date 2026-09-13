from database import Base
from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import relationship
class Author(Base):
    __tablename__='authors'
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    books=relationship('Book',back_populates='author',cascade="all, delete-orphan")
    is_active=Column(Boolean,nullable=False,default=True)
