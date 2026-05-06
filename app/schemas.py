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


from pydantic import BaseModel

# request schema
class UserCreate(BaseModel):
    name: str
    email: str

# response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True   # Pydantic v2 (important!)