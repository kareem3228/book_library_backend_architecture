from database import Base
from sqlalchemy import Column,String,Integer,Enum,Boolean
from enums.user_enums import UserRole
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False,unique=True)
    password_hash=Column(String,nullable=False)
    role=Column(Enum(UserRole,name="user_role",values_callable=lambda enum: [member.value for member in enum]),nullable=False,default=UserRole.MEMBER)
    rentals=relationship("Rental",back_populates="user",cascade="all, delete-orphan")
    is_active=Column(Boolean,nullable=False,default=True)