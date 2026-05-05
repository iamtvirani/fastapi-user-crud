# from pydantic import BaseModel
# from typing import Optional

# class User(BaseModel):
#     id: int
#     name: str
#     email: str

# class UserCreate(BaseModel):
#     name: str
#     email: str

# # ⭐ NEW MODEL
# class UserUpdate(BaseModel):
#     name: Optional[str] = None
#     email: Optional[str] = None

from sqlalchemy import Column, Integer, String
from .database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)