# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     name: str
#     email: str

# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: str

#     class Config:
#         orm_mode = True

from pydantic import BaseModel, EmailStr
from typing import Optional

# Create request
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Update request
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str